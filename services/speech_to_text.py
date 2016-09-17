from gcloud.credentials import get_credentials
from google.cloud.speech.v1beta1 import cloud_speech_pb2 as cloud_speech
from google.rpc import code_pb2
from grpc.beta import implementations

# Audio recording parameters
RATE = 16000
CHANNELS = 1
CHUNK = int(RATE / 10)  # 100ms

# Keep the request alive for this many seconds
DEADLINE_SECS = 8 * 60 * 60
SPEECH_SCOPE = 'https://www.googleapis.com/auth/cloud-platform'

class SpeechToText:
    """Provides audio streaming to the Google Cloud Speech API via GRPC.
    Based on the Google streaming example from:
    https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/speech/grpc/transcribe_streaming.py"""

    def __init__(self):
        self.establish_connection()

    def make_channel(self, host, port):
        """Creates an SSL channel with auth credentials from the environment."""
        # In order to make an https call, use an ssl channel with defaults
        ssl_channel = implementations.ssl_channel_credentials(None, None, None)

        # Grab application default credentials from the environment
        creds = get_credentials().create_scoped([SPEECH_SCOPE])
        # Add a plugin to inject the creds into the header
        auth_header = (
            'Authorization',
            'Bearer ' + creds.get_access_token().access_token)
        auth_plugin = implementations.metadata_call_credentials(
            lambda _, cb: cb([auth_header], None),
            name='google_creds')

        # compose the two together for both ssl and google auth
        composite_channel = implementations.composite_channel_credentials(
            ssl_channel, auth_plugin)

        return implementations.secure_channel(host, port, composite_channel)

    def request_stream(self, channels=CHANNELS, rate=RATE, chunk=CHUNK):
        """Yields `StreamingRecognizeRequest`s constructed from a recording audio
        stream.

        Args:
            stop_audio: A threading.Event object stops the recording when set.
            channels: How many audio channels to record.
            rate: The sampling rate in hertz.
            chunk: Buffer audio into chunks of this size before sending to the api.
        """
        # The initial request must contain metadata about the stream, so the
        # server knows how to interpret it.
        recognition_config = cloud_speech.RecognitionConfig(
            # There are a bunch of config options you can specify. See
            # https://goo.gl/KPZn97 for the full list.
            encoding='LINEAR16',  # raw 16-bit signed LE samples
            sample_rate=rate,  # the rate in hertz
            # See
            # https://g.co/cloud/speech/docs/best-practices#language_support
            # for a list of supported languages.
            language_code='en-US',  # a BCP-47 language tag
        )
        streaming_config = cloud_speech.StreamingRecognitionConfig(
            config=recognition_config,
        )

        yield cloud_speech.StreamingRecognizeRequest(
            streaming_config=streaming_config)

    def listen_print_loop(self, recognize_stream):
        for resp in recognize_stream:
            if resp.error.code != code_pb2.OK:
                raise RuntimeError('Server error: ' + resp.error.message)

            # TODO: remove debug output
            # Display the transcriptions & their alternatives
            for result in resp.results:
                print(result.alternatives)

    def handle_chunk(self, chunk):
        yield cloud_speech.StreamingRecognizeRequest(audio_content=chunk)

    def establish_connection(self):
        with cloud_speech.beta_create_Speech_stub(
                self.make_channel('speech.googleapis.com', 443)) as service:
            try:
                self.listen_print_loop(
                    service.StreamingRecognize(
                        self.request_stream(), DEADLINE_SECS))
            finally:
                # Stop the request stream once we're done with the loop - otherwise
                # it'll keep going in the thread that the grpc lib makes for it..
                print 'FINALLY'
