# SPDX-FileCopyrightText: Copyright (c) 2026, NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

import tempfile
import unittest
from pathlib import Path

import native_chunks


class NativeChunkPackagingTest(unittest.TestCase):
    def test_removes_stale_chunks_when_source_is_small_or_missing(self):
        for source_exists in (True, False):
            with self.subTest(source_exists=source_exists):
                with tempfile.TemporaryDirectory() as directory:
                    library = Path(directory) / "libcudf.so"
                    library.write_bytes(b"a" * 2048)
                    self.assertTrue(native_chunks.produce(library, 0, 1024, 9, 2))
                    chunks = Path(str(library) + ".chunks")
                    manifest = Path(str(library) + ".chunks.properties")
                    self.assertTrue(chunks.exists())
                    self.assertTrue(manifest.exists())

                    if source_exists:
                        library.write_bytes(b"b" * 1024)
                    self.assertFalse(native_chunks.produce(library, 2048, 1024, 9, 2))
                    self.assertEqual(source_exists, library.exists())
                    self.assertFalse(chunks.exists())
                    self.assertFalse(manifest.exists())


if __name__ == "__main__":
    unittest.main()
