from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any, List

from app.core.database import get_db
from app.core.security import get_current_user

# Import service (will be created in parallel)
from app.services.admin_service import AdminService

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
)


async def verify_admin(
    current_user: Dict[str, Any] = Depends(get_current_user),
) -> Dict[str, Any]:
    """
    Verify that current user has admin role.

    Args:
        current_user: Current authenticated user

    Returns:
        Current user if admin

    Raises:
        HTTPException: If user is not admin
    """
    role = current_user.get("role")
    if role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )

    return current_user


@router.get(
    "/users",
    response_model=List[Dict[str, Any]],
    summary="List all users",
)
async def list_users(
    admin: Dict[str, Any] = Depends(verify_admin),
    db: AsyncSession = Depends(get_db),
) -> List[Dict[str, Any]]:
    """
    List all users (admin only).

    Args:
        admin: Admin user verification
        db: Database session

    Returns:
        List of user details
    """
    admin_service = AdminService(db)

    try:
        users = await admin_service.list_users()
        return users
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving users",
        )


@router.post(
    "/templates",
    response_model=Dict[str, Any],
    status_code=status.HTTP_201_CREATED,
    summary="Create question template",
)
async def create_template(
    template_data: Dict[str, Any],
    admin: Dict[str, Any] = Depends(verify_admin),
    db: AsyncSession = Depends(get_db),
) -> Dict[str, Any]:
    """
    Create a new question template (admin only).

    Args:
        template_data: Template data
        admin: Admin user verification
        db: Database session

    Returns:
        Created template
    """
    admin_service = AdminService(db)

    try:
        template = await admin_service.create_template(template_data)
        return template
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.put(
    "/templates/{template_id}",
    response_model=Dict[str, Any],
    summary="Update question template",
)
async def update_template(
    template_id: int,
    template_data: Dict[str, Any],
    admin: Dict[str, Any] = Depends(verify_admin),
    db: AsyncSession = Depends(get_db),
) -> Dict[str, Any]:
    """
    Update an existing question template (admin only).

    Args:
        template_id: Template ID
        template_data: Updated template data
        admin: Admin user verification
        db: Database session

    Returns:
        Updated template

    Raises:
        HTTPException: If template not found
    """
    admin_service = AdminService(db)

    try:
        template = await admin_service.update_template(template_id, template_data)

        if not template:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Template not found",
            )

        return template
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get(
    "/stats",
    response_model=Dict[str, Any],
    summary="Get platform statistics",
)
async def get_stats(
    admin: Dict[str, Any] = Depends(verify_admin),
    db: AsyncSession = Depends(get_db),
) -> Dict[str, Any]:
    """
    Get platform statistics (admin only).

    Args:
        admin: Admin user verification
        db: Database session

    Returns:
        Platform statistics
    """
    admin_service = AdminService(db)

    try:
        stats = await admin_service.get_platform_stats()
        return stats
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving statistics",
        )
