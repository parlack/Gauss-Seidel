"""Tests for equation validators"""

import numpy as np
import pytest
from utils.validators import EquationValidator


class TestEquationValidator:
    """Test cases for EquationValidator"""

    def test_validate_valid_matrix(self):
        """Test validation of a valid matrix"""
        matrix_data = [["4", "1"], ["1", "3"]]
        is_valid, message, matrix = EquationValidator.validate_matrix(matrix_data)
        
        assert is_valid
        assert message == "matriz valida"
        assert matrix is not None
        assert matrix.shape == (2, 2)

    def test_validate_empty_matrix(self):
        """Test validation of empty matrix"""
        matrix_data = []
        is_valid, message, matrix = EquationValidator.validate_matrix(matrix_data)
        
        assert not is_valid
        assert "vacia" in message
        assert matrix is None

    def test_validate_non_square_matrix(self):
        """Test validation of non-square matrix"""
        matrix_data = [["1", "2", "3"], ["4", "5", "6"]]
        is_valid, message, matrix = EquationValidator.validate_matrix(matrix_data)
        
        assert not is_valid
        assert "cuadrada" in message
        assert matrix is None

    def test_validate_valid_vector(self):
        """Test validation of valid vector"""
        vector_data = ["1", "2"]
        is_valid, message, vector = EquationValidator.validate_vector(vector_data)
        
        assert is_valid
        assert message == "vector valido"
        assert vector is not None
        assert len(vector) == 2

    def test_validate_empty_vector(self):
        """Test validation of empty vector"""
        vector_data = []
        is_valid, message, vector = EquationValidator.validate_vector(vector_data)
        
        assert not is_valid
        assert "vacio" in message
        assert vector is None

    def test_make_diagonally_dominant(self):
        """Test making matrix diagonally dominant"""
        A = np.array([[1, 4], [6, 2]], dtype=float)
        b = np.array([5, 8], dtype=float)
        
        result = EquationValidator.make_diagonally_dominant(A, b)
        
        assert 'success' in result
        assert 'matrix' in result
        assert 'vector' in result
        assert 'swaps_made' in result
        assert 'message' in result
