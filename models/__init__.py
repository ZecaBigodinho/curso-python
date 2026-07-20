"""
CourseForge — Models Package
Modelos de domínio da plataforma.
"""
from .course import Course
from .module import Module
from .chapter import Chapter

__all__ = ["Course", "Module", "Chapter"]
