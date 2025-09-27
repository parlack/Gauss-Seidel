"""Tests for main module"""

import pytest
from unittest.mock import patch, MagicMock
import main


class TestMain:
    """Test cases for main module functions"""

    def test_check_dependencies_success(self):
        """Test dependency checking when all deps are available"""
        with patch('main.messagebox') as mock_messagebox:
            result = main.check_dependencies()
            assert result is True
            mock_messagebox.assert_not_called()

    @patch('main.messagebox')
    @patch('main.tk.Tk')
    def test_show_error_dialog(self, mock_tk, mock_messagebox):
        """Test error dialog display"""
        mock_root = MagicMock()
        mock_tk.return_value = mock_root
        
        main.show_error_dialog("Test Title", "Test Message")
        
        mock_tk.assert_called_once()
        mock_root.withdraw.assert_called_once()
        mock_messagebox.showerror.assert_called_once_with("Test Title", "Test Message")
        mock_root.destroy.assert_called_once()

    @patch('main.messagebox.askokcancel')
    @patch('main.sys.exit')
    def test_setup_closing_protocol(self, mock_exit, mock_askokcancel):
        """Test closing protocol setup"""
        mock_app = MagicMock()
        mock_askokcancel.return_value = True
        
        main.setup_closing_protocol(mock_app)
        
        # Get the callback function that was set
        protocol_call = mock_app.protocol.call_args
        assert protocol_call[0][0] == "WM_DELETE_WINDOW"
        
        # Test the callback
        callback = protocol_call[0][1]
        callback()
        
        mock_askokcancel.assert_called_once()
        mock_app.quit.assert_called_once()
        mock_app.destroy.assert_called_once()
        mock_exit.assert_called_once_with(0)
