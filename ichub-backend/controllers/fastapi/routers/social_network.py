#################################################################################
# Eclipse Tractus-X - Industry Core Hub Backend
#
# Copyright (c) 2025 Contributors to the Eclipse Foundation
#
# See the NOTICE file(s) distributed with this work for additional
# information regarding copyright ownership.
#
# This program and the accompanying materials are made available under the
# terms of the Apache License, Version 2.0 which is available at
# https://www.apache.org/licenses/LICENSE-2.0.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the
# License for the specific language govern in permissions and limitations
# under the License.
#
# SPDX-License-Identifier: Apache-2.0
#################################################################################

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
import uuid
from typing import List, Dict, Any, Optional
import datetime

# Import Tractus-X SDK components
from tractusx_sdk.industry.services.aas_service import AasService
from tractusx_sdk.industry.services.auth_service import AuthService
from tractusx_sdk.industry.models.aas.v3 import (
    AssetKind,
    ShellDescriptor,
    SubModelDescriptor,
    SpecificAssetId,
    Reference,
    ReferenceTypes,
    ProtocolInformation,
    Endpoint
)

# Create API router
router = APIRouter(
    prefix="/social-network",
    tags=["Social Network"],
    responses={404: {"description": "Not found"}},
)

# Sample in-memory data store (replace with database in production)
profiles = {}
posts = {}
friends = {}

# Models
class ApiKeyAuthService(AuthService):
    """API Key authentication service implementation"""
    
    def __init__(self, api_key: str):
        """Initialize with API key"""
        self.api_key = api_key
        
    def get_token(self) -> str:
        """Get the authentication token"""
        return self.api_key
        
    def is_token_valid(self) -> bool:
        """API keys don't expire"""
        return True

class SocialProfile(BaseModel):
    profile_name: str
    business_name: str
    bpn: str

class Post(BaseModel):
    content: str

class Friend(BaseModel):
    friend_profile_id: str

class DTRConfig(BaseModel):
    dtr_url: str
    api_key: str
    simulate: bool = False

# Route to get all profiles
@router.get("/profiles")
async def get_profiles():
    """Get all social network profiles"""
    return {"profiles": list(profiles.values())}

# Route to create a profile
@router.post("/profiles")
async def create_profile(profile: SocialProfile):
    """Create a new social network profile"""
    profile_id = str(uuid.uuid4())
    posts_id = str(uuid.uuid4())
    friends_id = str(uuid.uuid4())
    
    profile_data = {
        "profileId": f"urn:uuid:{profile_id}",
        "profileName": profile.profile_name,
        "businessName": profile.business_name,
        "businessPartner": profile.bpn
    }
    
    posts_data = {
        "postsId": f"urn:uuid:{posts_id}",
        "posts": []
    }
    
    friends_data = {
        "friendsId": f"urn:uuid:{friends_id}",
        "friends": []
    }
    
    # Store in our in-memory database
    profiles[profile_id] = profile_data
    posts[posts_id] = posts_data
    friends[friends_id] = friends_data
    
    return {
        "profile_id": profile_id,
        "posts_id": posts_id,
        "friends_id": friends_id,
        "profile": profile_data
    }

# Route to add a post
@router.post("/profiles/{profile_id}/posts")
async def add_post(profile_id: str, post: Post):
    """Add a post to a profile"""
    if profile_id not in profiles:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    # Find the posts_id for this profile
    for p_id, posts_data in posts.items():
        if posts_data.get("postsId") == f"urn:uuid:{profile_id}":
            post_id = str(uuid.uuid4())
            now = datetime.datetime.now()
            
            new_post = {
                "postId": f"urn:uuid:{post_id}",
                "content": post.content,
                "createdOn": now.strftime("%Y-%m-%d"),
                "lastModifiedOn": now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            }
            
            posts[p_id]["posts"].append(new_post)
            return new_post
    
    raise HTTPException(status_code=404, detail="Posts collection not found for this profile")

# Route to register with Digital Twin Registry
@router.post("/profiles/{profile_id}/register")
async def register_with_dtr(profile_id: str, config: DTRConfig):
    """Register a profile with the Digital Twin Registry"""
    if profile_id not in profiles:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    profile_data = profiles[profile_id]
    
    # Find associated posts and friends IDs
    posts_id = None
    friends_id = None
    
    for p_id, data in posts.items():
        if data.get("postsId") == f"urn:uuid:{profile_id}":
            posts_id = p_id
            break
    
    for f_id, data in friends.items():
        if data.get("friendsId") == f"urn:uuid:{profile_id}":
            friends_id = f_id
            break
    
    if not posts_id or not friends_id:
        raise HTTPException(status_code=500, detail="Could not find associated data")
    
    # If in simulation mode, just return the data
    if config.simulate:
        return {
            "message": "SIMULATION MODE - Would register with DTR",
            "profile": profile_data,
            "posts": posts[posts_id],
            "friends": friends[friends_id]
        }
    
    # Otherwise, register with DTR
    try:
        # Create auth service
        auth_service = ApiKeyAuthService(config.api_key)
        
        # Create AAS service
        aas_service = AasService(
            base_url=config.dtr_url,
            base_lookup_url=config.dtr_url,
            api_path="/api/v3",
            auth_service=auth_service,
            verify_ssl=False  # For development only
        )
        
        # Create shell descriptor
        shell_id = profile_id
        
        # Create specific asset IDs
        asset_ids = [
            SpecificAssetId(
                name="Profile",
                value=f"urn:uuid:{profile_id}"
            ),
            SpecificAssetId(
                name="Posts",
                value=f"urn:uuid:{posts_id}"
            ),
            SpecificAssetId(
                name="Friends",
                value=f"urn:uuid:{friends_id}"
            ),
            SpecificAssetId(
                name="BPN",
                value=profile_data["businessPartner"]
            )
        ]
        
        # Create shell descriptor
        shell = ShellDescriptor(
            id=f"urn:uuid:{shell_id}",
            id_short=f"SocialProfile_{profile_data['profileName']}",
            description=[],
            global_asset_id=f"urn:uuid:{shell_id}",
            specific_asset_ids=asset_ids,
            submodel_descriptors=[],
            asset_type="urn:tractusx:socialnetwork.user:1.0.0",
            asset_kind=AssetKind.INSTANCE
        )
        
        # Add submodels
        endpoint_url = f"http://localhost:8000/social-network/submodels"
        
        # Security attributes
        security_attr = {
            "type": "NONE",
            "key": "NONE",
            "value": "NONE"
        }
        
        # Create submodels
        # Profile submodel
        profile_protocol = ProtocolInformation(
            href=f"{endpoint_url}/profile/{profile_id}",
            endpoint_protocol="HTTP",
            endpoint_protocol_version=["1.1"],
            subprotocol="DSP",
            subprotocol_body=f"id=profile-{profile_id};dspEndpoint={endpoint_url}",
            subprotocol_body_encoding="plain",
            security_attributes=[security_attr]
        )
        
        profile_submodel = SubModelDescriptor(
            id=f"urn:uuid:{profile_id}",
            id_short="Profile",
            description=[],
            semantic_id=Reference(
                type=ReferenceTypes.EXTERNAL_REFERENCE,
                keys=[{
                    "type": "GlobalReference",
                    "value": "urn:samm:io.tractusx.socialnetwork_profile:1.0.0#Profile"
                }]
            ),
            endpoints=[
                Endpoint(
                    interface="SUBMODEL-3.0",
                    protocol_information=profile_protocol
                )
            ]
        )
        
        # Posts submodel
        posts_protocol = ProtocolInformation(
            href=f"{endpoint_url}/posts/{posts_id}",
            endpoint_protocol="HTTP",
            endpoint_protocol_version=["1.1"],
            subprotocol="DSP",
            subprotocol_body=f"id=posts-{posts_id};dspEndpoint={endpoint_url}",
            subprotocol_body_encoding="plain",
            security_attributes=[security_attr]
        )
        
        posts_submodel = SubModelDescriptor(
            id=f"urn:uuid:{posts_id}",
            id_short="Posts",
            description=[],
            semantic_id=Reference(
                type=ReferenceTypes.EXTERNAL_REFERENCE,
                keys=[{
                    "type": "GlobalReference",
                    "value": "urn:samm:io.tractusx.socialnetwork_posts:1.0.0#Posts"
                }]
            ),
            endpoints=[
                Endpoint(
                    interface="SUBMODEL-3.0",
                    protocol_information=posts_protocol
                )
            ]
        )
        
        # Friends submodel
        friends_protocol = ProtocolInformation(
            href=f"{endpoint_url}/friends/{friends_id}",
            endpoint_protocol="HTTP",
            endpoint_protocol_version=["1.1"],
            subprotocol="DSP",
            subprotocol_body=f"id=friends-{friends_id};dspEndpoint={endpoint_url}",
            subprotocol_body_encoding="plain",
            security_attributes=[security_attr]
        )
        
        friends_submodel = SubModelDescriptor(
            id=f"urn:uuid:{friends_id}",
            id_short="Friends",
            description=[],
            semantic_id=Reference(
                type=ReferenceTypes.EXTERNAL_REFERENCE,
                keys=[{
                    "type": "GlobalReference",
                    "value": "urn:samm:io.tractusx.socialnetwork_friends:1.0.0#Friend"
                }]
            ),
            endpoints=[
                Endpoint(
                    interface="SUBMODEL-3.0",
                    protocol_information=friends_protocol
                )
            ]
        )
        
        # Add submodels to shell
        shell.submodel_descriptors = [profile_submodel, posts_submodel, friends_submodel]
        
        # Register with DTR
        result = aas_service.create_asset_administration_shell_descriptor(shell)
        
        return {
            "message": "Successfully registered with DTR",
            "shell_id": shell_id,
            "dtr_url": config.dtr_url
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error registering with DTR: {str(e)}")

# Endpoint to provide submodel data
@router.get("/submodels/profile/{profile_id}")
async def get_profile_submodel(profile_id: str):
    """Get profile submodel data"""
    if profile_id not in profiles:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    return profiles[profile_id]

@router.get("/submodels/posts/{posts_id}")
async def get_posts_submodel(posts_id: str):
    """Get posts submodel data"""
    if posts_id not in posts:
        raise HTTPException(status_code=404, detail="Posts not found")
    
    return posts[posts_id]

@router.get("/submodels/friends/{friends_id}")
async def get_friends_submodel(friends_id: str):
    """Get friends submodel data"""
    if friends_id not in friends:
        raise HTTPException(status_code=404, detail="Friends not found")
    
    return friends[friends_id] 