"""
Computer-X-Control: LLM-Powered PC Automation Tool

This package provides functionality to control a PC through natural language
instructions interpreted by Large Language Models (LLMs).
"""

__version__ = "1.0.0"
__author__ = "TheSatyam-Singh"

from .automation.pc_controller import PCController
from .llm.llm_interface import LLMInterface
from .parser.command_parser import CommandParser

__all__ = ["PCController", "LLMInterface", "CommandParser"]