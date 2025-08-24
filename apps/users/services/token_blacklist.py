from datetime import datetime, timezone as dt_timezone
from dataclasses import dataclass
from typing import Optional, Tuple, Union
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken

from common.enums import TokenFields

User = get_user_model()


@dataclass
class TokenResult:
    """Result of token operations."""
    success: bool
    error: Optional[str] = None


@dataclass
class TokenInfo:
    """Information extracted from an access token."""
    jti: str
    user_id: Optional[int]
    issued_at: datetime
    expires_at: datetime
    token_string: str


@dataclass
class OutstandingTokenData:
    """Data for creating an OutstandingToken."""
    token: str
    jti: str
    created_at: datetime
    expires_at: datetime
    user: Optional[User] = None


class TokenBlacklistService:
    """Service for blacklisting refresh tokens."""

    @staticmethod
    def blacklist_refresh_token(refresh_token_str: str) -> TokenResult:
        """
        Blacklist a refresh token.

        Args:
            refresh_token_str: The refresh token string to blacklist

        Returns:
            TokenResult with success status and optional error message
        """
        try:
            token = RefreshToken(refresh_token_str)
            token.blacklist()
            return TokenResult(success=True)
        except Exception as e:
            return TokenResult(success=False, error=str(e))


class AccessTokenBlacklistService:
    """Service for blacklisting access tokens."""

    @staticmethod
    def _extract_token_info(access_token: AccessToken, token_str: str) -> TokenInfo:
        """Extract relevant information from an access token."""
        return TokenInfo(
            jti=access_token[TokenFields.JTI.value],
            user_id=access_token.get(TokenFields.USER_ID.value),
            issued_at=datetime.fromtimestamp(
                access_token[TokenFields.IAT.value],
                tz=dt_timezone.utc
            ),
            expires_at=datetime.fromtimestamp(
                access_token[TokenFields.EXP.value],
                tz=dt_timezone.utc
            ),
            token_string=token_str
        )

    @staticmethod
    def _get_user(user_id: Optional[int]) -> Optional[User]:
        """Get user by ID, return None if not found or user_id is None."""
        if not user_id:
            return None

        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None

    @staticmethod
    def _create_outstanding_token(token_info: TokenInfo) -> OutstandingToken:
        """Create an OutstandingToken from token information."""
        user = AccessTokenBlacklistService._get_user(token_info.user_id)

        outstanding_data = OutstandingTokenData(
            token=token_info.token_string,
            jti=token_info.jti,
            created_at=token_info.issued_at,
            expires_at=token_info.expires_at,
            user=user
        )

        return OutstandingToken.objects.create(
            token=outstanding_data.token,
            jti=outstanding_data.jti,
            created_at=outstanding_data.created_at,
            expires_at=outstanding_data.expires_at,
            user=outstanding_data.user,
        )

    @staticmethod
    def _get_or_create_outstanding_token(token_info: TokenInfo) -> OutstandingToken:
        """Get existing or create new OutstandingToken."""
        try:
            return OutstandingToken.objects.get(jti=token_info.jti)
        except OutstandingToken.DoesNotExist:
            return AccessTokenBlacklistService._create_outstanding_token(token_info)

    @staticmethod
    def blacklist(access_token_str: str) -> TokenResult:
        """
        Blacklist an access token.

        Args:
            access_token_str: The access token string to blacklist

        Returns:
            TokenResult with success status and optional error message
        """
        try:
            access_token = AccessToken(access_token_str)
            token_info = AccessTokenBlacklistService._extract_token_info(
                access_token, access_token_str
            )

            outstanding_token = AccessTokenBlacklistService._get_or_create_outstanding_token(
                token_info
            )

            BlacklistedToken.objects.get_or_create(token=outstanding_token)
            return TokenResult(success=True)

        except Exception as e:
            return TokenResult(success=False, error=str(e))