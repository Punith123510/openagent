"""Whatsapp chat data loader"""

import logging
from pathlib import Path
from typing import List

from openagent.knowledgebase.document_loaders.basereader import BaseReader
from openagent.schema import DocumentNode


class WhatsappChatLoader(BaseReader):
    """
    Whatsapp chat data loader.

    Args:
        path (str): Path to Whatsapp chat file.
    """

    def __init__(self, path: str):
        """Initialize with path."""

        self.file_path = path

    def load_data(self) -> List[DocumentNode]:
        """
        Parse Whatsapp file into Documents
        """

        from chatminer.chatparsers import WhatsAppParser

        path = Path(self.file_path)

        parser = WhatsAppParser(path)
        parser.parse_file()
        df = parser.parsed_messages.get_df()

        logging.debug(f"> Number of messages: {len(df)}.")

        docs = []
        n = 0
        for row in df.itertuples():
            extra_info = {
                "source": str(path).split("/")[-1].replace(".txt", ""),
                "author": row.author,
                "timestamp": str(row.timestamp),
            }

            docs.append(
                DocumentNode(
                    text=str(row.timestamp)
                    + " "
                    + row.author
                    + ":"
                    + " "
                    + row.message,
                    extra_info=extra_info,
                )
            )

            n += 1
            logging.debug(f"Added {n} of {len(df)} messages.")

        logging.debug(f"> DocumentNode creation for {path} is complete.")
        return docs
