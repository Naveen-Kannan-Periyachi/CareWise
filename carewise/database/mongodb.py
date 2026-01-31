"""MongoDB database connection and models."""
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
from typing import Optional, List, Dict, Any
import os
import bcrypt

# MongoDB connection
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = "carewise"

client = None
database = None

def get_database():
    """Get database instance."""
    global client, database
    if database is None:
        client = AsyncIOMotorClient(MONGODB_URL)
        database = client[DATABASE_NAME]
    return database

async def close_database():
    """Close database connection."""
    global client
    if client:
        client.close()

# Collections
def get_users_collection():
    """Get users collection."""
    db = get_database()
    return db.users

def get_conversations_collection():
    """Get conversations collection."""
    db = get_database()
    return db.conversations

def get_messages_collection():
    """Get messages collection."""
    db = get_database()
    return db.messages

# User operations
async def create_user(name: str, email: str, password: str) -> Dict[str, Any]:
    """Create a new user."""
    users = get_users_collection()
    
    # Check if user exists
    existing = await users.find_one({"email": email})
    if existing:
        raise ValueError("Email already registered")
    
    # Hash password (truncate to 72 bytes for bcrypt limit)
    password_bytes = password[:72].encode('utf-8')
    password_hash = bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode('utf-8')
    
    user_doc = {
        "name": name,
        "email": email,
        "password_hash": password_hash,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    result = await users.insert_one(user_doc)
    user_doc["_id"] = str(result.inserted_id)
    del user_doc["password_hash"]
    
    return user_doc

async def authenticate_user(email: str, password: str) -> Optional[Dict[str, Any]]:
    """Authenticate user with email and password."""
    users = get_users_collection()
    user = await users.find_one({"email": email})
    
    if not user:
        return None
    
    # Verify password (truncate to 72 bytes for bcrypt limit)
    password_bytes = password[:72].encode('utf-8')
    password_hash_bytes = user["password_hash"].encode('utf-8')
    if not bcrypt.checkpw(password_bytes, password_hash_bytes):
        return None
    
    user["_id"] = str(user["_id"])
    del user["password_hash"]
    return user

async def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    """Get user by email."""
    users = get_users_collection()
    user = await users.find_one({"email": email})
    
    if user:
        user["_id"] = str(user["_id"])
        if "password_hash" in user:
            del user["password_hash"]
    
    return user

# Conversation operations
async def create_conversation(user_email: str, title: str = "New Chat") -> Dict[str, Any]:
    """Create a new conversation."""
    conversations = get_conversations_collection()
    
    conv_doc = {
        "user_email": user_email,
        "title": title,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    result = await conversations.insert_one(conv_doc)
    conv_doc["_id"] = str(result.inserted_id)
    
    return conv_doc

async def get_user_conversations(user_email: str) -> List[Dict[str, Any]]:
    """Get all conversations for a user."""
    conversations = get_conversations_collection()
    cursor = conversations.find({"user_email": user_email}).sort("updated_at", -1)
    
    convs = []
    async for conv in cursor:
        conv["_id"] = str(conv["_id"])
        convs.append(conv)
    
    return convs

async def update_conversation_title(conversation_id: str, title: str) -> bool:
    """Update conversation title."""
    from bson import ObjectId
    conversations = get_conversations_collection()
    
    result = await conversations.update_one(
        {"_id": ObjectId(conversation_id)},
        {"$set": {"title": title, "updated_at": datetime.utcnow()}}
    )
    
    return result.modified_count > 0

async def delete_conversation(conversation_id: str, user_email: str) -> bool:
    """Delete a conversation and its messages."""
    from bson import ObjectId
    conversations = get_conversations_collection()
    messages = get_messages_collection()
    
    # Delete messages first
    await messages.delete_many({"conversation_id": conversation_id})
    
    # Delete conversation
    result = await conversations.delete_one({
        "_id": ObjectId(conversation_id),
        "user_email": user_email
    })
    
    return result.deleted_count > 0

# Message operations
async def create_message(
    conversation_id: str,
    role: str,
    content: str,
    evidence: Optional[List[Dict[str, Any]]] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Create a new message in a conversation."""
    messages = get_messages_collection()
    conversations = get_conversations_collection()
    from bson import ObjectId
    
    msg_doc = {
        "conversation_id": conversation_id,
        "role": role,
        "content": content,
        "evidence": evidence or [],
        "metadata": metadata or {},
        "created_at": datetime.utcnow()
    }
    
    result = await messages.insert_one(msg_doc)
    msg_doc["_id"] = str(result.inserted_id)
    
    # Update conversation's updated_at
    await conversations.update_one(
        {"_id": ObjectId(conversation_id)},
        {"$set": {"updated_at": datetime.utcnow()}}
    )
    
    return msg_doc

async def get_conversation_messages(conversation_id: str) -> List[Dict[str, Any]]:
    """Get all messages in a conversation."""
    messages = get_messages_collection()
    cursor = messages.find({"conversation_id": conversation_id}).sort("created_at", 1)
    
    msgs = []
    async for msg in cursor:
        msg["_id"] = str(msg["_id"])
        msgs.append(msg)
    
    return msgs

async def delete_conversation_messages(conversation_id: str) -> int:
    """Delete all messages in a conversation."""
    messages = get_messages_collection()
    result = await messages.delete_many({"conversation_id": conversation_id})
    return result.deleted_count
