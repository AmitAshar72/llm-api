import logging
from typing import Optional
from .backends.factory import BackendFactory
from .backends.base import BackendError, BackendNotAvailableError
from .config import settings

logger = logging.getLogger(__name__)

async def generate_response(prompt: str, backend_type: Optional[str] = None) -> str:
    print(f"[GENERATOR] Called with prompt: {prompt}")
    try:
        backend = BackendFactory.get_backend()
        print(f"[GENERATOR] Using backend: {backend.name}")
        logger.info(f"Using backend: {backend.name}")
        logger.debug(f"Generating response for prompt: {prompt[:100]}...")
        response = await backend.generate(prompt)
        print(f"[GENERATOR] Backend response: {response}")
        logger.debug(f"Generated response length: {len(response)}")
        return response
    except BackendError as e:
        print(f"[GENERATOR] BackendError: {e}")
        logger.error(f"Backend error: {e}")
        try:
            stub_backend = BackendFactory.get_backend(settings.BackendType.STUB)
            fallback_response = await stub_backend.generate(prompt)
            print(f"[GENERATOR] Fallback to stub backend: {fallback_response}")
            logger.warning(f"Falling back to stub backend: {fallback_response}")
            return fallback_response
        except Exception as fallback_error:
            print(f"[GENERATOR] Stub backend failed: {fallback_error}")
            logger.error(f"Even stub backend failed: {fallback_error}")
            return f"Error: Unable to generate response. {str(e)}"
    except Exception as e:
        print(f"[GENERATOR] Unexpected error: {e}")
        logger.error(f"Unexpected error in generate_response: {e}")
        return f"Error: Unexpected error occurred. {str(e)}" 