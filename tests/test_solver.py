"""Tests for the Gauss-Seidel solver"""

import numpy as np
import pytest
from solver.gauss_seidel import GaussSeidelSolver


class TestGaussSeidelSolver:
    """Test cases for GaussSeidelSolver"""

    def setup_method(self):
        """Set up test fixtures"""
        self.solver = GaussSeidelSolver()

    def test_solver_initialization(self):
        """Test solver is properly initialized"""
        assert self.solver.max_iterations == 100
        assert self.solver.tolerance == 0.000001
        assert self.solver.iteration_history == []
        assert self.solver.error_history == []

    def test_simple_2x2_system(self):
        """Test solving a simple 2x2 system"""
        # System: 4x + y = 1, x + 3y = 2
        A = np.array([[4, 1], [1, 3]], dtype=float)
        b = np.array([1, 2], dtype=float)
        
        result = self.solver.solve(A, b)
        
        assert result['converged']
        assert len(result['solution']) == 2
        assert result['iterations'] > 0

    def test_diagonally_dominant_check(self):
        """Test diagonal dominance checking"""
        # Diagonally dominant matrix
        A_dominant = np.array([[4, 1], [1, 3]], dtype=float)
        assert self.solver._is_diagonally_dominant(A_dominant)
        
        # Non-diagonally dominant matrix
        A_non_dominant = np.array([[1, 4], [4, 1]], dtype=float)
        assert not self.solver._is_diagonally_dominant(A_non_dominant)

    def test_step_by_step_generation(self):
        """Test step-by-step solution generation"""
        A = np.array([[4, 1], [1, 3]], dtype=float)
        b = np.array([1, 2], dtype=float)
        
        steps = self.solver.generate_step_by_step(A, b)
        
        assert len(steps) > 0
        assert any(step['type'] == 'system' for step in steps)
        assert any(step['type'] == 'result' for step in steps)
