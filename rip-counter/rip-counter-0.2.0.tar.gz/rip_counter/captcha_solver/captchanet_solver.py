import os
import logging
import sys

from PIL import Image

from ..utils import open_archive


class CaptchaNetSolver:

  MODEL_URL = "https://storage.googleapis.com/hadim-data/models/captchanet-rip-v4.zip"

  def __init__(self, model_location=None, preload_model=True, display_image=False, verbose=False):

    self.log = logging.getLogger('CaptchaNetSolver')
    self.log.setLevel(logging.INFO)

    self.model_path = None
    self.tokenizer_path = None
    self.model = None

    if model_location:
      self._get_archive(model_location)
    else:
      self._get_archive(CaptchaNetSolver.MODEL_URL)

    self.display_image = display_image
    self.verbose = verbose

    if preload_model:
      self._load_model()

  def _init_tensorflow(self):
    if "tensorflow" not in sys.modules:
      self.log.info("Initialize Tensorflow")

      import tensorflow as tf
      os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
      tf.get_logger().setLevel(logging.ERROR)

      # Remove logging handler for tf/absl.
      import absl
      import absl.logging
      # pylint: disable=protected-access
      logging.root.removeHandler(absl.logging._absl_handler)
      # pylint: disable=protected-access
      absl.logging._warn_preinit_stderr = False

      import rip_counter
      rip_counter.setup_logging(silent=True)

  def _get_archive(self, model_location):
    self.log.info(f"Retrieve the model archive from {model_location}.")
    model_dir = open_archive(model_location, progressbar=True)
    self.model_path = model_dir / "model.h5"
    self.tokenizer_path = model_dir / "tokenizer"

  def _load_model(self):

    if not self.model:
      self._init_tensorflow()

      import tensorflow as tf
      import tensorflow_datasets as tfds

      self.log.info("Load the CaptchaNet model in memory.")
      self.tokenizer = tfds.features.text.TokenTextEncoder.load_from_file(str(self.tokenizer_path))
      tf.keras.backend.clear_session()
      self.model = tf.keras.models.load_model(str(self.model_path))
      self.log.info("CaptchaNet correctly loaded.")

  def __call__(self, image):

    import tensorflow as tf

    self._load_model()

    if self.display_image:
      from IPython.display import display

      display(Image.fromarray(image))

    # Preprocess the image
    batch = tf.cast([image], 'float32')
    batch = tf.image.per_image_standardization(batch)

    # Run inference
    labels = self.model(batch)

    # Postprocess results (decode labels)
    labels = tf.argmax(labels, axis=2)
    labels = [self.tokenizer.decode(label) for label in labels]
    labels = [label.replace(' ', '').replace('0', '') for label in labels]

    if self.verbose:
      self.log.info(f"Predicted {labels[0]} ({len(labels[0])})")

    return labels[0]
