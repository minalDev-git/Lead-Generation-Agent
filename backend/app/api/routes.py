from fastapi import APIRouter
from app.services.parser import prompt_parser
from app.models import PromptRequest
from app.services.browser import launch_browser
router = APIRouter(
    prefix="/api",
    tags=["Lead Generation"]
)

@router.post("/parse-prompt")
def ask(request: PromptRequest):
    result = prompt_parser(request.prompt)
    return result

# POST /api/browser-test
@router.post("/browser-test")
async def browse(parsed: dict):
    try:
        # 1. Launch Browser
        businesses = await launch_browser(parsed)
        
        return {
            "status": "success",
            "total": len(businesses),
            "businesses": businesses
        }
        
    except Exception as e:
        return {"status": "error", "message": str(e)}
    


@router.get("/test")
def test():
    return {
        "message": "FastAPI routes are working!"
    }