"""
Discord Webhook Library
A simple library for sending messages to Discord channels via webhooks.

Usage:
    from events.system.webhook_lib import DiscordWebhook
    
    webhook = DiscordWebhook("https://discord.com/api/webhooks/...")
    await webhook.send("Hello World!")
"""

import aiohttp
import asyncio
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

class DiscordWebhook:
    """Simple Discord webhook client"""
    
    def __init__(self, webhook_url: str):
        """
        Initialize webhook client
        
        Args:
            webhook_url: Discord webhook URL
        """
        self.webhook_url = webhook_url
    
    async def send(self, 
                   content: str, 
                   username: Optional[str] = None,
                   avatar_url: Optional[str] = None,
                   embeds: Optional[list] = None) -> bool:
        """
        Send a message via webhook
        
        Args:
            content: Message content
            username: Custom username for the webhook
            avatar_url: Custom avatar URL for the webhook
            embeds: List of Discord embeds
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            payload = {"content": content}
            
            if username:
                payload["username"] = username
            if avatar_url:
                payload["avatar_url"] = avatar_url
            if embeds:
                payload["embeds"] = embeds
            
            async with aiohttp.ClientSession() as session:
                async with session.post(self.webhook_url, json=payload) as response:
                    if response.status == 204:
                        logger.info(f"✅ Webhook message sent: {content[:50]}...")
                        return True
                    else:
                        logger.error(f"❌ Webhook failed with status {response.status}")
                        return False
                        
        except aiohttp.ClientError as e:
            logger.error(f"❌ Network error: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ Unexpected error: {e}")
            return False
    
    def send_sync(self, content: str, username: Optional[str] = None) -> bool:
        """
        Synchronous wrapper for send method
        
        Args:
            content: Message content
            username: Custom username for the webhook
            
        Returns:
            bool: True if successful, False otherwise
        """
        return asyncio.run(self.send(content, username))


# Convenience functions for quick usage
async def send_message(webhook_url: str, content: str, username: str = "Python Bot") -> bool:
    """
    Quick function to send a webhook message
    
    Args:
        webhook_url: Discord webhook URL
        content: Message content
        username: Custom username
        
    Returns:
        bool: Success status
    """
    webhook = DiscordWebhook(webhook_url)
    return await webhook.send(content, username)


def send_message_sync(webhook_url: str, content: str, username: str = "Python Bot") -> bool:
    """
    Synchronous version of send_message
    
    Args:
        webhook_url: Discord webhook URL
        content: Message content
        username: Custom username
        
    Returns:
        bool: Success status
    """
    return asyncio.run(send_message(webhook_url, content, username))
