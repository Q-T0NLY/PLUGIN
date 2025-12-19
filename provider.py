"""
CodeGen provider abstraction for Chatbox CodeGen integration.
Provides a simple interface used by chat UI to request code-generation, preview, and chain-of-thought outputs.
This module chooses an adapter (Codespaces, Google AI, or demo) and exposes a consistent API.
"""
from typing import Dict, Optional, Any
import asyncio
import logging

logger = logging.getLogger("hyper_registry.chatbox.codegen.provider")


class CodeGenProvider:
    """High-level provider that delegates to a selected adapter.

    Adapter must implement async methods:
      - generate_code(prompt: str, context: Dict) -> Dict
      - preview_render(result: Dict) -> Dict
      - explain_chain_of_thought(prompt: str, context: Dict) -> Dict
    """

    def __init__(self, adapter: Any = None):
        self.adapter = adapter
        if adapter:
            logger.info(f"[🎯] CodeGenProvider: adapter set to {adapter.__class__.__name__}")
        else:
            logger.info("[🎯] CodeGenProvider: no adapter provided, using demo stub")

    def set_adapter(self, adapter: Any):
        self.adapter = adapter
        logger.info(f"[🎯] CodeGenProvider: adapter switched to {adapter.__class__.__name__}")

    async def generate_code(self, prompt: str, context: Optional[Dict] = None) -> Dict:
        context = context or {}
        if self.adapter and hasattr(self.adapter, "generate_code"):
            return await self.adapter.generate_code(prompt, context)
        return await self._demo_generate(prompt, context)

    async def preview_render(self, result: Dict) -> Dict:
        if self.adapter and hasattr(self.adapter, "preview_render"):
            return await self.adapter.preview_render(result)
        return await self._demo_preview(result)

    async def explain_chain_of_thought(self, prompt: str, context: Optional[Dict] = None) -> Dict:
        context = context or {}
        if self.adapter and hasattr(self.adapter, "explain_chain_of_thought"):
            return await self.adapter.explain_chain_of_thought(prompt, context)
        return await self._demo_chain_of_thought(prompt, context)

    # --- Demo fallbacks ---
    async def _demo_generate(self, prompt: str, context: Dict) -> Dict:
        """Return a deterministic demo response (safe for offline demos)."""
        await asyncio.sleep(0.05)
        demo_code = f"# Demo generated code for prompt:\n# {prompt[:120]}\nprint('Hello from demo CodeGen')\n"
        return {
            "success": True,
            "source": "demo",
            "prompt": prompt,
            "code": demo_code,
            "metadata": {"length": len(demo_code), "language": "python"}
        }

    async def _demo_preview(self, result: Dict) -> Dict:
        await asyncio.sleep(0.01)
        # simple preview payload: first lines, visual cues
        code = result.get("code", "")
        preview = "\n".join(code.splitlines()[:8])
        return {"preview": preview, "visual": {"type": "text", "style": "monospace"}}

    async def _demo_chain_of_thought(self, prompt: str, context: Dict) -> Dict:
        await asyncio.sleep(0.02)
        steps = [
            "Parse prompt and detect intent",
            "Extract code context (files, symbols)",
            "Plan generation steps (stubs, helpers, tests)",
            "Emit code with docstrings and minimal tests",
        ]
        return {"prompt": prompt, "cot_steps": steps}
