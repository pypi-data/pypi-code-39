ARCHIVE_EOF     = 1   # Found end of archive.
ARCHIVE_OK      = 0   # Operation was successful.
ARCHIVE_RETRY   = -10 # Retry might succeed.
ARCHIVE_WARN    = -20 # Partial success.
ARCHIVE_FAILED  = -25 # Current operation cannot complete.
ARCHIVE_FATAL   = -30 # No more operations are possible.

ARCHIVE_FILTER_NONE     = 0
ARCHIVE_FILTER_GZIP     = 1
ARCHIVE_FILTER_BZIP2    = 2
ARCHIVE_FILTER_COMPRESS = 3
ARCHIVE_FILTER_PROGRAM  = 4
ARCHIVE_FILTER_LZMA     = 5
ARCHIVE_FILTER_XZ       = 6
ARCHIVE_FILTER_UU       = 7
ARCHIVE_FILTER_RPM      = 8
ARCHIVE_FILTER_LZIP     = 9
ARCHIVE_FILTER_LRZIP    = 10
ARCHIVE_FILTER_LZOP     = 11
ARCHIVE_FILTER_GRZIP    = 12

ARCHIVE_FORMAT_BASE_MASK           = 0xff0000
ARCHIVE_FORMAT_CPIO                = 0x10000
ARCHIVE_FORMAT_CPIO_POSIX          = (ARCHIVE_FORMAT_CPIO | 1)
ARCHIVE_FORMAT_CPIO_BIN_LE         = (ARCHIVE_FORMAT_CPIO | 2)
ARCHIVE_FORMAT_CPIO_BIN_BE         = (ARCHIVE_FORMAT_CPIO | 3)
ARCHIVE_FORMAT_CPIO_SVR4_NOCRC     = (ARCHIVE_FORMAT_CPIO | 4)
ARCHIVE_FORMAT_CPIO_SVR4_CRC       = (ARCHIVE_FORMAT_CPIO | 5)
ARCHIVE_FORMAT_CPIO_AFIO_LARGE     = (ARCHIVE_FORMAT_CPIO | 6)
ARCHIVE_FORMAT_SHAR                = 0x20000
ARCHIVE_FORMAT_SHAR_BASE           = (ARCHIVE_FORMAT_SHAR | 1)
ARCHIVE_FORMAT_SHAR_DUMP           = (ARCHIVE_FORMAT_SHAR | 2)
ARCHIVE_FORMAT_TAR                 = 0x30000
ARCHIVE_FORMAT_TAR_USTAR           = (ARCHIVE_FORMAT_TAR | 1)
ARCHIVE_FORMAT_TAR_PAX_INTERCHANGE = (ARCHIVE_FORMAT_TAR | 2)
ARCHIVE_FORMAT_TAR_PAX_RESTRICTED  = (ARCHIVE_FORMAT_TAR | 3)
ARCHIVE_FORMAT_TAR_GNUTAR          = (ARCHIVE_FORMAT_TAR | 4)
ARCHIVE_FORMAT_ISO9660             = 0x40000
ARCHIVE_FORMAT_ISO9660_ROCKRIDGE   = (ARCHIVE_FORMAT_ISO9660 | 1)
ARCHIVE_FORMAT_ZIP                 = 0x50000
ARCHIVE_FORMAT_EMPTY               = 0x60000
ARCHIVE_FORMAT_AR                  = 0x70000
ARCHIVE_FORMAT_AR_GNU              = (ARCHIVE_FORMAT_AR | 1)
ARCHIVE_FORMAT_AR_BSD              = (ARCHIVE_FORMAT_AR | 2)
ARCHIVE_FORMAT_MTREE               = 0x80000
ARCHIVE_FORMAT_RAW                 = 0x90000
ARCHIVE_FORMAT_XAR                 = 0xA0000
ARCHIVE_FORMAT_LHA                 = 0xB0000
ARCHIVE_FORMAT_CAB                 = 0xC0000
ARCHIVE_FORMAT_RAR                 = 0xD0000
ARCHIVE_FORMAT_7ZIP                = 0xE0000
