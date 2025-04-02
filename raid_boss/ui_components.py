from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.resources import resource_find
from typing import List, Optional
import os
from dataclasses import dataclass
from enum import Enum, auto

# Get the path to the fonts directory in the root of the repo
FONT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "fonts")
FONT_PATH = os.path.join(FONT_DIR, "Beleren2016-Bold.ttf")  # Replace with your font filename


class TextType(Enum):
    GAME_STATE = auto()
    BOSS_ATTACK = auto()
    PLAYER_ACTION = auto()
    ERROR = auto()
    PROMPT = auto()


@dataclass
class GameText:
    content: str
    text_type: TextType
    timestamp: float
    priority: int = 0  # Higher priority text appears first


class GameTextManager:
    def __init__(self):
        self.text_buffer: List[GameText] = []
        self.max_buffer_size = 1000  # Prevent memory issues with very long games
        self._output_callback = None

    def set_output_callback(self, callback):
        """Set the callback function to update the UI when text changes."""
        self._output_callback = callback

    def add_text(self, content: str, text_type: TextType, priority: int = 0) -> None:
        """Add new text to the buffer and update the display."""
        from time import time

        new_text = GameText(content=content, text_type=text_type, timestamp=time(), priority=priority)
        self.text_buffer.append(new_text)

        # Keep buffer size manageable
        if len(self.text_buffer) > self.max_buffer_size:
            self.text_buffer = self.text_buffer[-self.max_buffer_size :]

        # Update display
        self._update_display()

    def clear(self) -> None:
        """Clear all text from the buffer."""
        self.text_buffer.clear()
        self._update_display()

    def _update_display(self) -> None:
        """Update the display with formatted text."""
        if self._output_callback is None:
            return

        # Sort text by timestamp (oldest first) to maintain chronological order
        sorted_text = sorted(self.text_buffer, key=lambda x: x.timestamp)

        # Format text with appropriate spacing and styling
        formatted_text = ""
        for text in sorted_text:
            if text.text_type == TextType.ERROR:
                formatted_text += f"{text.content}\n\n"
            elif text.text_type == TextType.BOSS_ATTACK:
                formatted_text += f"{text.content}\n\n"
            elif text.text_type == TextType.PROMPT:
                formatted_text += f"{text.content}\n"
            else:
                formatted_text += f"{text.content}\n\n"

        self._output_callback(formatted_text)


class GameOutput(Label):
    text = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.text_size = (None, None)
        self.halign = "left"
        self.valign = "bottom"
        self.bind(text=self._on_text_change)
        self._scroll_view = None
        self.color = (1, 1, 1, 1)
        self.padding = [10, 10, 10, 10]
        self.text_size = (self.width, None)
        self.limit_render_to_text_bbox = False  # Allow text to expand beyond visible area
        self.markup = True  # Enable markup for color tags

        # Set custom font
        if os.path.exists(FONT_PATH):
            self.font_name = FONT_PATH
        else:
            self.font_name = "RobotoMono"
            print(f"Warning: Custom font not found at {FONT_PATH}. Using system font.")

        # Add dark background
        with self.canvas.before:
            Color(0.1, 0.1, 0.1, 1)
            self.rect = Rectangle(pos=self.pos, size=self.size)

        self.bind(pos=self._update_rect, size=self._update_rect)

    def _update_text(self, new_text: str) -> None:
        """Update the text property with new content."""
        self.text = new_text
        # Schedule scroll to bottom after text update
        Clock.schedule_once(self._scroll_to_bottom, 0.1)

    def add_text(self, content: str, text_type: TextType, priority: int = 0) -> None:
        """Add new text to the output."""
        # Format the text based on type
        if text_type == TextType.ERROR:
            formatted_text = f"[color=ff4444]{content}[/color]\n\n"
        elif text_type == TextType.BOSS_ATTACK:
            formatted_text = f"[color=ffaa00]{content}[/color]\n\n"
        elif text_type == TextType.PROMPT:
            formatted_text = f"[color=44ff44]{content}[/color]\n"
        else:
            formatted_text = f"{content}\n\n"

        # Append the new text to existing text
        self.text = self.text + formatted_text
        # Schedule scroll to bottom
        Clock.schedule_once(self._scroll_to_bottom, 0.1)

    def clear(self) -> None:
        """Clear all text from the output."""
        self.text = ""
        Clock.schedule_once(self._scroll_to_bottom, 0.1)

    def _update_rect(self, instance, value):
        """Update the background rectangle and text size when position or size changes."""
        self.rect.pos = instance.pos
        self.rect.size = instance.size
        self.text_size = (self.width, None)
        # Ensure text height is updated
        Clock.schedule_once(self._update_height, 0.1)

    def _update_height(self, dt):
        """Update the height based on content."""
        if self.texture_size[1] > 0:
            self.height = self.texture_size[1] + 20  # Add padding
            # Ensure scroll view updates
            if self._scroll_view:
                self._scroll_view.scroll_y = 0

    def _on_text_change(self, instance, value):
        """Handle text changes and update layout."""
        # Schedule height update after text change
        Clock.schedule_once(self._update_height, 0.1)

    def _scroll_to_bottom(self, dt):
        """Scroll to the bottom of the text."""
        if self._scroll_view:
            # Force a layout update by temporarily disabling and re-enabling vertical scrolling
            self._scroll_view.do_scroll_y = False
            self._scroll_view.do_scroll_y = True
            # Set scroll position to bottom
            self._scroll_view.scroll_y = 0
            # Force a second scroll after a short delay to ensure it works
            Clock.schedule_once(lambda dt: setattr(self._scroll_view, "scroll_y", 0), 0.1)

    def set_scroll_view(self, scroll_view):
        """Set the scroll view reference."""
        self._scroll_view = scroll_view


class GameInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height = 40
        self.multiline = False
        self.focus = True  # Set initial focus

        if os.path.exists(FONT_PATH):
            self.font_name = FONT_PATH
        else:
            self.font_name = "RobotoMono"
            print(f"Warning: Custom font not found at {FONT_PATH}. Using system font.")

        self.background_color = (0.2, 0.2, 0.2, 1)
        self.foreground_color = (1, 1, 1, 1)
        self.cursor_color = (1, 1, 1, 1)
        self.padding = [10, 10, 10, 10]

    def on_text_validate(self):
        """Handle text validation and maintain focus."""
        # Ensure focus is maintained after validation
        Clock.schedule_once(lambda dt: setattr(self, "focus", True), 0.1)


class GameInterface(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = 0
        self.spacing = 0

        # Create a container for the scroll view with padding
        self.scroll_container = BoxLayout(orientation="vertical", size_hint=(1, 1))
        self.scroll_container.padding = [0, 0, 0, 50]  # Add padding at bottom to prevent text from being hidden

        # Create scroll view
        self.scroll = ScrollView(
            size_hint=(1, 1),
            do_scroll_x=False,
            do_scroll_y=True,
            bar_width=10,
            bar_color=(1, 1, 1, 1),
            bar_inactive_color=(0.2, 0.2, 0.2, 1),
            effect_cls="ScrollEffect",
            scroll_type=["bars", "content"],
        )

        # Create output widget
        self.output = GameOutput()
        self.output.set_scroll_view(self.scroll)

        # Add output to scroll view
        self.scroll.add_widget(self.output)

        # Add scroll view to container
        self.scroll_container.add_widget(self.scroll)

        # Create input box
        self.input_box = GameInput()

        # Bind input box events
        self.input_box.bind(on_text_validate=self._on_input_validate)
        Window.bind(on_touch_down=self._on_touch_down)

        # Add widgets to layout
        self.add_widget(self.scroll_container)
        self.add_widget(self.input_box)

        # Bind window resize
        Window.bind(on_resize=self._on_window_resize)

    def _on_input_validate(self, instance):
        """Handle input validation and maintain focus."""
        # Clear the input box
        instance.text = ""
        # Ensure focus is maintained
        Clock.schedule_once(lambda dt: setattr(instance, "focus", True), 0.1)

    def _on_touch_down(self, instance, touch):
        """Handle touch events to maintain focus on input box."""
        # If the touch is not on the input box, return focus to it
        if not self.input_box.collide_point(*touch.pos):
            self.input_box.focus = True

    def _on_window_resize(self, instance, width, height):
        """Handle window resize events."""
        # Update scroll container size
        self.scroll_container.size = (width, height - self.input_box.height)
        # Ensure scroll position is updated
        Clock.schedule_once(self.output._scroll_to_bottom, 0.1)
        # Ensure input box maintains focus
        Clock.schedule_once(lambda dt: setattr(self.input_box, "focus", True), 0.1)
