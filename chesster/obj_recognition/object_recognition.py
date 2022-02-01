from pathlib import Path
import logging
import os
from typing import Union, Optional
import numpy as np
from chesster.master.module import Module
from chesster.obj_recognition.chessboard_recognition import *
from chesster.obj_recognition.chessboard import *
from chesster.obj_recognition.chesspiece import ChessPiece

logger = logging.getLogger(__name__)


class ObjectRecognition(Module):
    def __init__(self, board_info_path: Union[str, os.PathLike], debug=False):
        logger.info('Initializing Object recognition module!')
        self.board_info_path = board_info_path
        self.board = ChessBoard.load(Path(board_info_path))
        self.debug = debug
        logger.info('Chessboard recognition module initialized!')

    def stop(self):
        logger.info('Stopping Object recognition module!')
        logger.info('Object recognition module stopped!')

    def start(self):
        self.board.start()
        logger.info('Starting Object recognition module!')
        logger.info('Chessboard recognition module started!')

    def determine_changes(self, previous: np.ndarray, current_image: np.ndarray):
        move = self.board.determine_changes(previous, current_image, self.debug)
        return self.get_chessboard_matrix()

    def get_chesspiece_info(self, chessfield: str, depth_map) -> Optional[ChessPiece]:
        for field in self.board.fields:
            if field.position == chessfield:
                width, height = self.board.image.shape[:2]
                zenith = field.get_zenith(depth_map, width, height)
                chesspiece = ChessPiece(field.position, field.contour, zenith)
                return chesspiece
        return None

    def get_chessboard_matrix(self):
        return self.board.current_chess_matrix

    def get_fields(self):
        return self.board.fields

    @staticmethod
    def create_chessboard_data(image, depth, output_path: Path, debug=False):
        board = ChessboardRecognition.from_image(image, depth_map=depth, debug=debug)
        board.save(output_path)