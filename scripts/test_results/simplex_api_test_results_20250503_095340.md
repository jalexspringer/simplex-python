# SimpleX WebSocket API Test Results

Test date: 2025-05-03 09:53:41

## Overview

This document contains the results of testing various SimpleX WebSocket API commands. Each section contains different categories of commands and their respective responses.

### Table of Contents

- [User Commands](#user-commands)
- [Profile Commands](#profile-commands)
- [Address Commands](#address-commands)
- [Chat Commands](#chat-commands)
- [Group Commands](#group-commands)
- [Contact Commands](#contact-commands)
- [Message Commands](#message-commands)
- [Server Protocol Commands](#server-protocol-commands)
- [Database Commands](#database-commands)
- [File Commands](#file-commands)
- [Miscellaneous Commands](#miscellaneous-commands)

### Request Format

All commands are sent as WebSocket messages with the following JSON format:

```json
{
  "corrId": "123",
  "cmd": "command string"
}
```

Where:
- `corrId`: A correlation ID to match responses to requests
- `cmd`: The command string to execute

### Response Format

Responses are also JSON objects with the following structure:

```json
{
  "corrId": "123",
  "resp": {
    "type": "responseType",
    ...
  }
}
```

Where:
- `corrId`: The correlation ID from the request
- `resp`: The response object containing various fields depending on the command


## User Commands

### Show Active User

**Command:** `/u`

**Status:** ✅ Success

**Response:**
```json
{
  "resp": {
    "type": "userContactSubSummary",
    "user": {
      "userId": 1,
      "agentUserId": "1",
      "userContactId": 1,
      "localDisplayName": "BOT1_UPDATED",
      "profile": {
        "profileId": 1,
        "displayName": "BOT1_UPDATED",
        "fullName": "Bot One Updated",
        "image": "",
        "localAlias": ""
      },
      "fullPreferences": {
        "timedMessages": {
          "allow": "yes"
        },
        "fullDelete": {
          "allow": "no"
        },
        "reactions": {
          "allow": "yes"
        },
        "voice": {
          "allow": "yes"
        },
        "calls": {
          "allow": "yes"
        }
      },
      "activeUser": true,
      "activeOrder": 4,
      "showNtfs": true,
      "sendRcptsContacts": true,
      "sendRcptsSmallGroups": true,
      "userMemberProfileUpdatedAt": "2025-05-03T08:42:55.098428Z"
    },
    "userContactSubscriptions": []
  }
}
```

**Response Type:** `userContactSubSummary`

### List Users

**Command:** `/users`

**Status:** ✅ Success

**Response:**
```json
{
  "resp": {
    "type": "groupEmpty",
    "user": {
      "userId": 1,
      "agentUserId": "1",
      "userContactId": 1,
      "localDisplayName": "BOT1_UPDATED",
      "profile": {
        "profileId": 1,
        "displayName": "BOT1_UPDATED",
        "fullName": "Bot One Updated",
        "image": "",
        "localAlias": ""
      },
      "fullPreferences": {
        "timedMessages": {
          "allow": "yes"
        },
        "fullDelete": {
          "allow": "no"
        },
        "reactions": {
          "allow": "yes"
        },
        "voice": {
          "allow": "yes"
        },
        "calls": {
          "allow": "yes"
        }
      },
      "activeUser": true,
      "activeOrder": 4,
      "showNtfs": true,
      "sendRcptsContacts": true,
      "sendRcptsSmallGroups": true,
      "userMemberProfileUpdatedAt": "2025-05-03T08:42:55.098428Z"
    },
    "shortGroupInfo": {
      "groupId": 1,
      "groupName": "Test",
      "membershipStatus": "creator"
    }
  }
}
```

**Response Type:** `groupEmpty`

### Create Active User

**Command:** `/_create user {"profile": {"displayName": "TEST_USER", "fullName": "Test User"}, "sameServers": true, "pastTimestamp": false}`

**Status:** ✅ Success

**Response:**
```json
{
  "resp": {
    "type": "groupEmpty",
    "user": {
      "userId": 1,
      "agentUserId": "1",
      "userContactId": 1,
      "localDisplayName": "BOT1_UPDATED",
      "profile": {
        "profileId": 1,
        "displayName": "BOT1_UPDATED",
        "fullName": "Bot One Updated",
        "image": "",
        "localAlias": ""
      },
      "fullPreferences": {
        "timedMessages": {
          "allow": "yes"
        },
        "fullDelete": {
          "allow": "no"
        },
        "reactions": {
          "allow": "yes"
        },
        "voice": {
          "allow": "yes"
        },
        "calls": {
          "allow": "yes"
        }
      },
      "activeUser": true,
      "activeOrder": 4,
      "showNtfs": true,
      "sendRcptsContacts": true,
      "sendRcptsSmallGroups": true,
      "userMemberProfileUpdatedAt": "2025-05-03T08:42:55.098428Z"
    },
    "shortGroupInfo": {
      "groupId": 2,
      "groupName": "Test_1",
      "membershipStatus": "creator"
    }
  }
}
```

**Response Type:** `groupEmpty`

### Hide User

**Command:** `/_hide user 1 "password"`

**Status:** ✅ Success

**Response:**
```json
{
  "resp": {
    "type": "groupEmpty",
    "user": {
      "userId": 1,
      "agentUserId": "1",
      "userContactId": 1,
      "localDisplayName": "BOT1_UPDATED",
      "profile": {
        "profileId": 1,
        "displayName": "BOT1_UPDATED",
        "fullName": "Bot One Updated",
        "image": "",
        "localAlias": ""
      },
      "fullPreferences": {
        "timedMessages": {
          "allow": "yes"
        },
        "fullDelete": {
          "allow": "no"
        },
        "reactions": {
          "allow": "yes"
        },
        "voice": {
          "allow": "yes"
        },
        "calls": {
          "allow": "yes"
        }
      },
      "activeUser": true,
      "activeOrder": 4,
      "showNtfs": true,
      "sendRcptsContacts": true,
      "sendRcptsSmallGroups": true,
      "userMemberProfileUpdatedAt": "2025-05-03T08:42:55.098428Z"
    },
    "shortGroupInfo": {
      "groupId": 3,
      "groupName": "Test_2",
      "membershipStatus": "creator"
    }
  }
}
```

**Response Type:** `groupEmpty`

### Unhide User

**Command:** `/_unhide user 1 "password"`

**Status:** ✅ Success

**Response:**
```json
{
  "resp": {
    "type": "memberSubSummary",
    "user": {
      "userId": 1,
      "agentUserId": "1",
      "userContactId": 1,
      "localDisplayName": "BOT1_UPDATED",
      "profile": {
        "profileId": 1,
        "displayName": "BOT1_UPDATED",
        "fullName": "Bot One Updated",
        "image": "",
        "localAlias": ""
      },
      "fullPreferences": {
        "timedMessages": {
          "allow": "yes"
        },
        "fullDelete": {
          "allow": "no"
        },
        "reactions": {
          "allow": "yes"
        },
        "voice": {
          "allow": "yes"
        },
        "calls": {
          "allow": "yes"
        }
      },
      "activeUser": true,
      "activeOrder": 4,
      "showNtfs": true,
      "sendRcptsContacts": true,
      "sendRcptsSmallGroups": true,
      "userMemberProfileUpdatedAt": "2025-05-03T08:42:55.098428Z"
    },
    "memberSubscriptions": []
  }
}
```

**Response Type:** `memberSubSummary`

### Mute User

**Command:** `/_mute user 1`

**Status:** ✅ Success

**Response:**
```json
{
  "resp": {
    "type": "pendingSubSummary",
    "user": {
      "userId": 1,
      "agentUserId": "1",
      "userContactId": 1,
      "localDisplayName": "BOT1_UPDATED",
      "profile": {
        "profileId": 1,
        "displayName": "BOT1_UPDATED",
        "fullName": "Bot One Updated",
        "image": "",
        "localAlias": ""
      },
      "fullPreferences": {
        "timedMessages": {
          "allow": "yes"
        },
        "fullDelete": {
          "allow": "no"
        },
        "reactions": {
          "allow": "yes"
        },
        "voice": {
          "allow": "yes"
        },
        "calls": {
          "allow": "yes"
        }
      },
      "activeUser": true,
      "activeOrder": 4,
      "showNtfs": true,
      "sendRcptsContacts": true,
      "sendRcptsSmallGroups": true,
      "userMemberProfileUpdatedAt": "2025-05-03T08:42:55.098428Z"
    },
    "pendingSubscriptions": []
  }
}
```

**Response Type:** `pendingSubSummary`

### Unmute User

**Command:** `/_unmute user 1`

**Status:** ✅ Success

**Response:**
```json
{
  "resp": {
    "type": "contactSubSummary",
    "user": {
      "userId": 2,
      "agentUserId": "2",
      "userContactId": 5,
      "localDisplayName": "TEST_USER",
      "profile": {
        "profileId": 5,
        "displayName": "TEST_USER",
        "fullName": "Test User",
        "localAlias": ""
      },
      "fullPreferences": {
        "timedMessages": {
          "allow": "yes"
        },
        "fullDelete": {
          "allow": "no"
        },
        "reactions": {
          "allow": "yes"
        },
        "voice": {
          "allow": "yes"
        },
        "calls": {
          "allow": "yes"
        }
      },
      "activeUser": false,
      "activeOrder": 2,
      "showNtfs": true,
      "sendRcptsContacts": true,
      "sendRcptsSmallGroups": true
    },
    "contactSubscriptions": []
  }
}
```

**Response Type:** `contactSubSummary`

### Set Active User

**Command:** `/_user 1`

**Status:** ✅ Success

**Response:**
```json
{
  "resp": {
    "type": "userContactSubSummary",
    "user": {
      "userId": 2,
      "agentUserId": "2",
      "userContactId": 5,
      "localDisplayName": "TEST_USER",
      "profile": {
        "profileId": 5,
        "displayName": "TEST_USER",
        "fullName": "Test User",
        "localAlias": ""
      },
      "fullPreferences": {
        "timedMessages": {
          "allow": "yes"
        },
        "fullDelete": {
          "allow": "no"
        },
        "reactions": {
          "allow": "yes"
        },
        "voice": {
          "allow": "yes"
        },
        "calls": {
          "allow": "yes"
        }
      },
      "activeUser": false,
      "activeOrder": 2,
      "showNtfs": true,
      "sendRcptsContacts": true,
      "sendRcptsSmallGroups": true
    },
    "userContactSubscriptions": []
  }
}
```

**Response Type:** `userContactSubSummary`


## Profile Commands

### Update Profile

**Command:** `/_profile 1 {"displayName": "BOT1_UPDATED", "fullName": "Bot One Updated", "image": ""}`

**Format:** `/_profile userId profileJson`

Updates the user's profile with new display name, full name, and image.

**Status:** ✅ Success

**Response:**
```json
{
  "resp": {
    "type": "memberSubSummary",
    "user": {
      "userId": 2,
      "agentUserId": "2",
      "userContactId": 5,
      "localDisplayName": "TEST_USER",
      "profile": {
        "profileId": 5,
        "displayName": "TEST_USER",
        "fullName": "Test User",
        "localAlias": ""
      },
      "fullPreferences": {
        "timedMessages": {
          "allow": "yes"
        },
        "fullDelete": {
          "allow": "no"
        },
        "reactions": {
          "allow": "yes"
        },
        "voice": {
          "allow": "yes"
        },
        "calls": {
          "allow": "yes"
        }
      },
      "activeUser": false,
      "activeOrder": 2,
      "showNtfs": true,
      "sendRcptsContacts": true,
      "sendRcptsSmallGroups": true
    },
    "memberSubscriptions": []
  }
}
```

**Response Type:** `memberSubSummary`


## Address Commands

### Create My Address

**Command:** `/_address 1`

**Status:** ✅ Success

**Response:**
```json
{
  "resp": {
    "type": "pendingSubSummary",
    "user": {
      "userId": 2,
      "agentUserId": "2",
      "userContactId": 5,
      "localDisplayName": "TEST_USER",
      "profile": {
        "profileId": 5,
        "displayName": "TEST_USER",
        "fullName": "Test User",
        "localAlias": ""
      },
      "fullPreferences": {
        "timedMessages": {
          "allow": "yes"
        },
        "fullDelete": {
          "allow": "no"
        },
        "reactions": {
          "allow": "yes"
        },
        "voice": {
          "allow": "yes"
        },
        "calls": {
          "allow": "yes"
        }
      },
      "activeUser": false,
      "activeOrder": 2,
      "showNtfs": true,
      "sendRcptsContacts": true,
      "sendRcptsSmallGroups": true
    },
    "pendingSubscriptions": []
  }
}
```

**Response Type:** `pendingSubSummary`

### Show My Address

**Command:** `/show_address`

**Status:** ✅ Success

**Response:**
```json
{
  "corrId": "1",
  "resp": {
    "type": "chats",
    "chats": [
      {
        "chatInfo": {
          "type": "direct",
          "contact": {
            "contactId": 4,
            "localDisplayName": "BOT2",
            "profile": {
              "profileId": 4,
              "displayName": "BOT2",
              "fullName": "",
              "preferences": {
                "timedMessages": {
                  "allow": "yes"
                },
                "fullDelete": {
                  "allow": "no"
                },
                "reactions": {
                  "allow": "yes"
                },
                "voice": {
                  "allow": "yes"
                },
                "calls": {
                  "allow": "yes"
                }
              },
              "localAlias": "BOT2_ALIAS"
            },
            "activeConn": {
              "connId": 2,
              "agentConnId": "MjhOZUlmVEFjSVBxR0VqQQ==",
              "connChatVersion": 14,
              "peerChatVRange": {
                "minVersion": 1,
                "maxVersion": 14
              },
              "connLevel": 0,
              "viaGroupLink": false,
              "connType": "contact",
              "connStatus": "ready",
              "contactConnInitiated": false,
              "localAlias": "",
              "entityId": 4,
              "pqSupport": true,
              "pqEncryption": true,
              "pqSndEnabled": true,
              "pqRcvEnabled": true,
              "authErrCounter": 0,
              "quotaErrCounter": 0,
              "createdAt": "2025-05-03T08:15:38.727032Z"
            },
            "contactUsed": true,
            "contactStatus": "active",
            "chatSettings": {
              "enableNtfs": "all",
              "favorite": false
            },
            "userPreferences": {},
            "mergedPreferences": {
              "timedMessages": {
                "enabled": {
                  "forUser": true,
                  "forContact": true
                },
                "userPreference": {
                  "type": "user",
                  "preference": {
                    "allow": "yes"
                  }
                },
                "contactPreference": {
                  "allow": "yes"
                }
              },
              "fullDelete": {
                "enabled": {
                  "forUser": false,
                  "forContact": false
                },
                "userPreference": {
                  "type": "user",
                  "preference": {
                    "allow": "no"
                  }
                },
                "contactPreference": {
                  "allow": "no"
                }
              },
              "reactions": {
                "enabled": {
                  "forUser": true,
                  "forContact": true
                },
                "userPreference": {
                  "type": "user",
                  "preference": {
                    "allow": "yes"
                  }
                },
                "contactPreference": {
                  "allow": "yes"
                }
              },
              "voice": {
                "enabled": {
                  "forUser": true,
                  "forContact": true
                },
                "userPreference": {
                  "type": "user",
                  "preference": {
                    "allow": "yes"
                  }
                },
                "contactPreference": {
                  "allow": "yes"
                }
              },
              "calls": {
                "enabled": {
                  "forUser": true,
                  "forContact": true
                },
                "userPreference": {
                  "type": "user",
                  "preference": {
                    "allow": "yes"
                  }
                },
                "contactPreference": {
                  "allow": "yes"
                }
              }
            },
            "createdAt": "2025-05-03T08:15:38.727032Z",
            "updatedAt": "2025-05-03T08:15:38.727032Z",
            "chatTs": "2025-05-03T08:53:01.343616Z",
            "contactGrpInvSent": false,
            "chatTags": [],
            "chatDeleted": false
          }
        },
        "chatItems": [
          {
            "chatDir": {
              "type": "directSnd"
            },
            "meta": {
              "itemId": 45,
              "itemTs": "2025-05-03T08:53:01.343616Z",
              "itemText": "# Heading\n**Bold text** and *italic text*\n```\ncode block\n```",
              "itemStatus": {
                "type": "sndRcvd",
                "msgRcptStatus": "ok",
                "sndProgress": "complete"
              },
              "sentViaProxy": false,
              "itemSharedMsgId": "d1NPUHVDSDAyVWVTNnVwUA==",
              "itemEdited": false,
              "userMention": false,
              "deletable": true,
              "editable": true,
              "createdAt": "2025-05-03T08:53:01.343616Z",
              "updatedAt": "2025-05-03T08:53:02.731548Z"
            },
            "content": {
              "type": "sndMsgContent",
              "msgContent": {
                "type": "text",
                "text": "# Heading\n**Bold text** and *italic text*\n```\ncode block\n```"
              }
            },
            "mentions": {},
            "formattedText": [
              {
                "text": "# Heading\n**Bold text** and "
              },
              {
                "format": {
                  "type": "bold"
                },
                "text": "italic text"
              },
              {
                "text": "\n```\ncode block\n```"
              }
            ],
            "reactions": []
          }
        ],
        "chatStats": {
          "unreadCount": 0,
          "unreadMentions": 0,
          "reportsCount": 0,
          "minUnreadItemId": 0,
          "unreadChat": false
        }
      },
      {
        "chatInfo": {
          "type": "group",
          "groupInfo": {
            "groupId": 3,
            "localDisplayName": "Test_2",
            "groupProfile": {
              "displayName": "Test",
              "fullName": "API Group Testing SimpleX WebSocket API None",
              "groupPreferences": {
                "directMessages": {
                  "enable": "on"
                },
                "history": {
                  "enable": "on"
                }
              }
            },
            "localAlias": "",
            "fullGroupPreferences": {
              "timedMessages": {
                "enable": "off",
                "ttl": 86400
              },
              "directMessages": {
                "enable": "on"
              },
              "fullDelete": {
                "enable": "off"
              },
              "reactions": {
                "enable": "on"
              },
              "voice": {
                "enable": "on"
              },
              "files": {
                "enable": "on"
              },
              "simplexLinks": {
                "enable": "on"
              },
              "reports": {
                "enable": "on"
              },
              "history": {
                "enable": "on"
              }
            },
            "membership": {
              "groupMemberId": 3,
              "groupId": 3,
              "memberId": "aExGdWRkQWNFa0hnTmhIZw==",
              "memberRole": "owner",
              "memberCategory": "user",
              "memberStatus": "creator",
              "memberSettings": {
                "showMessages": true
              },
              "blockedByAdmin": false,
              "invitedBy": {
                "type": "user"
              },
              "localDisplayName": "BOT1_UPDATED",
              "memberProfile": {
                "profileId": 1,
                "displayName": "BOT1_UPDATED",
                "fullName": "Bot One Updated",
                "image": "",
                "localAlias": ""
              },
              "memberContactId": 1,
              "memberContactProfileId": 1,
              "memberChatVRange": {
                "minVersion": 1,
                "maxVersion": 14
              },
              "createdAt": "2025-05-03T08:53:01.137225Z",
              "updatedAt": "2025-05-03T08:53:01.137225Z"
            },
            "chatSettings": {
              "enableNtfs": "all",
              "favorite": false
            },
            "createdAt": "2025-05-03T08:53:01.137225Z",
            "updatedAt": "2025-05-03T08:53:01.137225Z",
            "chatTs": "2025-05-03T08:53:01.162927Z",
            "userMemberProfileSentAt": "2025-05-03T08:53:01.137225Z",
            "chatTags": []
          }
        },
        "chatItems": [
          {
            "chatDir": {
              "type": "groupSnd"
            },
            "meta": {
              "itemId": 41,
              "itemTs": "2025-05-03T08:53:01.162927Z",
              "itemText": "Recent history: on",
              "itemStatus": {
                "type": "sndNew"
              },
              "itemEdited": false,
              "userMention": false,
              "deletable": false,
              "editable": false,
              "createdAt": "2025-05-03T08:53:01.162927Z",
              "updatedAt": "2025-05-03T08:53:01.162927Z"
            },
            "content": {
              "type": "sndGroupFeature",
              "groupFeature": "history",
              "preference": {
                "enable": "on"
              }
            },
            "mentions": {},
            "reactions": []
          }
        ],
        "chatStats": {
          "unreadCount": 0,
          "unreadMentions": 0,
          "reportsCount": 0,
          "minUnreadItemId": 0,
          "unreadChat": false
        }
      },
      {
        "chatInfo": {
          "type": "group",
          "groupInfo": {
            "groupId": 2,
            "localDisplayName": "Test_1",
            "groupProfile": {
              "displayName": "Test",
              "fullName": "API Group Testing SimpleX WebSocket API None",
              "groupPreferences": {
                "directMessages": {
                  "enable": "on"
                },
                "history": {
                  "enable": "on"
                }
              }
            },
            "localAlias": "",
            "fullGroupPreferences": {
              "timedMessages": {
                "enable": "off",
                "ttl": 86400
              },
              "directMessages": {
                "enable": "on"
              },
              "fullDelete": {
                "enable": "off"
              },
              "reactions": {
                "enable": "on"
              },
              "voice": {
                "enable": "on"
              },
              "files": {
                "enable": "on"
              },
              "simplexLinks": {
                "enable": "on"
              },
              "reports": {
                "enable": "on"
              },
              "history": {
                "enable": "on"
              }
            },
            "membership": {
              "groupMemberId": 2,
              "groupId": 2,
              "memberId": "bTBDdEJOUzJ4NTRNTTBTag==",
              "memberRole": "owner",
              "memberCategory": "user",
              "memberStatus": "creator",
              "memberSettings": {
                "showMessages": true
              },
              "blockedByAdmin": false,
              "invitedBy": {
                "type": "user"
              },
              "localDisplayName": "BOT1_UPDATED",
              "memberProfile": {
                "profileId": 1,
                "displayName": "BOT1_UPDATED",
                "fullName": "Bot One Updated",
                "image": "",
                "localAlias": ""
              },
              "memberContactId": 1,
              "memberContactProfileId": 1,
              "memberChatVRange": {
                "minVersion": 1,
                "maxVersion": 14
              },
              "createdAt": "2025-05-03T08:42:55.93582Z",
              "updatedAt": "2025-05-03T08:42:55.93582Z"
            },
            "chatSettings": {
              "enableNtfs": "all",
              "favorite": false
            },
            "createdAt": "2025-05-03T08:42:55.93582Z",
            "updatedAt": "2025-05-03T08:42:55.93582Z",
            "chatTs": "2025-05-03T08:42:55.956836Z",
            "userMemberProfileSentAt": "2025-05-03T08:42:55.93582Z",
            "chatTags": []
          }
        },
        "chatItems": [
          {
            "chatDir": {
              "type": "groupSnd"
            },
            "meta": {
              "itemId": 26,
              "itemTs": "2025-05-03T08:42:55.956836Z",
              "itemText": "Recent history: on",
              "itemStatus": {
                "type": "sndNew"
              },
              "itemEdited": false,
              "userMention": false,
              "deletable": false,
              "editable": false,
              "createdAt": "2025-05-03T08:42:55.956836Z",
              "updatedAt": "2025-05-03T08:42:55.956836Z"
            },
            "content": {
              "type": "sndGroupFeature",
              "groupFeature": "history",
              "preference": {
                "enable": "on"
              }
            },
            "mentions": {},
            "reactions": []
          }
        ],
        "chatStats": {
          "unreadCount": 0,
          "unreadMentions": 0,
          "reportsCount": 0,
          "minUnreadItemId": 0,
          "unreadChat": false
        }
      },
      {
        "chatInfo": {
          "type": "group",
          "groupInfo": {
            "groupId": 1,
            "localDisplayName": "Test",
            "groupProfile": {
              "displayName": "Test",
              "fullName": "Group Task-21 Test Group for Integration Tests None",
              "groupPreferences": {
                "directMessages": {
                  "enable": "on"
                },
                "history": {
                  "enable": "on"
                }
              }
            },
            "localAlias": "",
            "fullGroupPreferences": {
              "timedMessages": {
                "enable": "off",
                "ttl": 86400
              },
              "directMessages": {
                "enable": "on"
              },
              "fullDelete": {
                "enable": "off"
              },
              "reactions": {
                "enable": "on"
              },
              "voice": {
                "enable": "on"
              },
              "files": {
                "enable": "on"
              },
              "simplexLinks": {
                "enable": "on"
              },
              "reports": {
                "enable": "on"
              },
              "history": {
                "enable": "on"
              }
            },
            "membership": {
              "groupMemberId": 1,
              "groupId": 1,
              "memberId": "Ly9qeW1VU1AzVUw1OWpKag==",
              "memberRole": "owner",
              "memberCategory": "user",
              "memberStatus": "creator",
              "memberSettings": {
                "showMessages": true
              },
              "blockedByAdmin": false,
              "invitedBy": {
                "type": "user"
              },
              "localDisplayName": "BOT1_UPDATED",
              "memberProfile": {
                "profileId": 1,
                "displayName": "BOT1_UPDATED",
                "fullName": "Bot One Updated",
                "image": "",
                "localAlias": ""
              },
              "memberContactId": 1,
              "memberContactProfileId": 1,
              "memberChatVRange": {
                "minVersion": 1,
                "maxVersion": 14
              },
              "createdAt": "2025-05-03T08:36:07.479887Z",
              "updatedAt": "2025-05-03T08:42:55.098428Z"
            },
            "chatSettings": {
              "enableNtfs": "all",
              "favorite": false
            },
            "createdAt": "2025-05-03T08:36:07.479887Z",
            "updatedAt": "2025-05-03T08:36:07.479887Z",
            "chatTs": "2025-05-03T08:36:07.508595Z",
            "userMemberProfileSentAt": "2025-05-03T08:36:07.479887Z",
            "chatTags": []
          }
        },
        "chatItems": [
          {
            "chatDir": {
              "type": "groupSnd"
            },
            "meta": {
              "itemId": 16,
              "itemTs": "2025-05-03T08:36:07.508595Z",
              "itemText": "Recent history: on",
              "itemStatus": {
                "type": "sndNew"
              },
              "itemEdited": false,
              "userMention": false,
              "deletable": false,
              "editable": false,
              "createdAt": "2025-05-03T08:36:07.508595Z",
              "updatedAt": "2025-05-03T08:36:07.508595Z"
            },
            "content": {
              "type": "sndGroupFeature",
              "groupFeature": "history",
              "preference": {
                "enable": "on"
              }
            },
            "mentions": {},
            "reactions": []
          }
        ],
        "chatStats": {
          "unreadCount": 0,
          "unreadMentions": 0,
          "reportsCount": 0,
          "minUnreadItemId": 0,
          "unreadChat": false
        }
      },
      {
        "chatInfo": {
          "type": "direct",
          "contact": {
            "contactId": 3,
            "localDisplayName": "SimpleX Chat team",
            "profile": {
              "profileId": 3,
              "displayName": "SimpleX Chat team",
              "fullName": "",
              "image": "data:image/jpg;base64,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",
              "contactLink": "simplex:/contact#/?v=2&smp=smp%3A%2F%2FPQUV2eL0t7OStZOoAsPEV2QYWt4-xilbakvGUGOItUo%3D%40smp6.simplex.im%2FK1rslx-m5bpXVIdMZg9NLUZ_8JBm8xTt%23%2F%3Fv%3D1%26dh%3DMCowBQYDK2VuAyEALDeVe-sG8mRY22LsXlPgiwTNs9dbiLrNuA7f3ZMAJ2w%253D%26srv%3Dbylepyau3ty4czmn77q4fglvperknl4bi2eb2fdy2bh4jxtf32kf73yd.onion",
              "localAlias": ""
            },
            "contactUsed": true,
            "contactStatus": "active",
            "chatSettings": {
              "enableNtfs": "all",
              "favorite": false
            },
            "userPreferences": {},
            "mergedPreferences": {
              "timedMessages": {
                "enabled": {
                  "forUser": true,
                  "forContact": true
                },
                "userPreference": {
                  "type": "user",
                  "preference": {
                    "allow": "yes"
                  }
                },
                "contactPreference": {
                  "allow": "yes"
                }
              },
              "fullDelete": {
                "enabled": {
                  "forUser": false,
                  "forContact": false
                },
                "userPreference": {
                  "type": "user",
                  "preference": {
                    "allow": "no"
                  }
                },
                "contactPreference": {
                  "allow": "no"
                }
              },
              "reactions": {
                "enabled": {
                  "forUser": true,
                  "forContact": true
                },
                "userPreference": {
                  "type": "user",
                  "preference": {
                    "allow": "yes"
                  }
                },
                "contactPreference": {
                  "allow": "yes"
                }
              },
              "voice": {
                "enabled": {
                  "forUser": true,
                  "forContact": true
                },
                "userPreference": {
                  "type": "user",
                  "preference": {
                    "allow": "yes"
                  }
                },
                "contactPreference": {
                  "allow": "yes"
                }
              },
              "calls": {
                "enabled": {
                  "forUser": true,
                  "forContact": true
                },
                "userPreference": {
                  "type": "user",
                  "preference": {
                    "allow": "yes"
                  }
                },
                "contactPreference": {
                  "allow": "yes"
                }
              }
            },
            "createdAt": "2025-05-03T08:13:55.288057Z",
            "updatedAt": "2025-05-03T08:13:55.288057Z",
            "chatTs": "2025-05-03T08:13:55.288057Z",
            "contactGrpInvSent": false,
            "chatTags": [],
            "chatDeleted": false
          }
        },
        "chatItems": [],
        "chatStats": {
          "unreadCount": 0,
          "unreadMentions": 0,
          "reportsCount": 0,
          "minUnreadItemId": 0,
          "unreadChat": false
        }
      },
      {
        "chatInfo": {
          "type": "direct",
          "contact": {
            "contactId": 2,
            "localDisplayName": "SimpleX-Status",
            "profile": {
              "profileId": 2,
              "displayName": "SimpleX-Status",
              "fullName": "",
              "image": "data:image/jpg;base64,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",
              "contactLink": "simplex:/contact#/?v=2&smp=smp%3A%2F%2Fu2dS9sG8nMNURyZwqASV4yROM28Er0luVTx5X1CsMrU%3D%40smp4.simplex.im%2FShQuD-rPokbDvkyotKx5NwM8P3oUXHxA%23%2F%3Fv%3D1-2%26dh%3DMCowBQYDK2VuAyEA6fSx1k9zrOmF0BJpCaTarZvnZpMTAVQhd3RkDQ35KT0%253D%26srv%3Do5vmywmrnaxalvz6wi3zicyftgio6psuvyniis6gco6bp6ekl4cqj4id.onion",
              "localAlias": ""
            },
            "contactUsed": true,
            "contactStatus": "active",
            "chatSettings": {
              "enableNtfs": "all",
              "favorite": false
            },
            "userPreferences": {},
            "mergedPreferences": {
              "timedMessages": {
                "enabled": {
                  "forUser": true,
                  "forContact": true
                },
                "userPreference": {
                  "type": "user",
                  "preference": {
                    "allow": "yes"
                  }
                },
                "contactPreference": {
                  "allow": "yes"
                }
              },
              "fullDelete": {
                "enabled": {
                  "forUser": false,
                  "forContact": false
                },
                "userPreference": {
                  "type": "user",
                  "preference": {
                    "allow": "no"
                  }
                },
                "contactPreference": {
                  "allow": "no"
                }
              },
              "reactions": {
                "enabled": {
                  "forUser": true,
                  "forContact": true
                },
                "userPreference": {
                  "type": "user",
                  "preference": {
                    "allow": "yes"
                  }
                },
                "contactPreference": {
                  "allow": "yes"
                }
              },
              "voice": {
                "enabled": {
                  "forUser": true,
                  "forContact": true
                },
                "userPreference": {
                  "type": "user",
                  "preference": {
                    "allow": "yes"
                  }
                },
                "contactPreference": {
                  "allow": "yes"
                }
              },
              "calls": {
                "enabled": {
                  "forUser": true,
                  "forContact": true
                },
                "userPreference": {
                  "type": "user",
                  "preference": {
                    "allow": "yes"
                  }
                },
                "contactPreference": {
                  "allow": "yes"
                }
              }
            },
            "createdAt": "2025-05-03T08:13:55.287368Z",
            "updatedAt": "2025-05-03T08:13:55.287368Z",
            "chatTs": "2025-05-03T08:13:55.287368Z",
            "contactGrpInvSent": false,
            "chatTags": [],
            "chatDeleted": false
          }
        },
        "chatItems": [],
        "chatStats": {
          "unreadCount": 0,
          "unreadMentions": 0,
          "reportsCount": 0,
          "minUnreadItemId": 0,
          "unreadChat": false
        }
      },
      {
        "chatInfo": {
          "type": "local",
          "noteFolder": {
            "noteFolderId": 1,
            "userId": 1,
            "createdAt": "2025-05-03T08:13:55Z",
            "updatedAt": "2025-05-03T08:13:55Z",
            "chatTs": "2025-05-03T08:13:55Z",
            "favorite": false,
            "unread": false
          }
        },
        "chatItems": [],
        "chatStats": {
          "unreadCount": 0,
          "unreadMentions": 0,
          "reportsCount": 0,
          "minUnreadItemId": 0,
          "unreadChat": false
        }
      }
    ]
  }
}
```

**Response Type:** `chats`

### Set Profile Address (enable)

**Command:** `/profile_address on`

**Status:** ✅ Success

**Response:**
```json
{
  "corrId": "2",
  "resp": {
    "type": "activeUser",
    "user": {
      "userId": 1,
      "agentUserId": "1",
      "userContactId": 1,
      "localDisplayName": "BOT1_UPDATED",
      "profile": {
        "profileId": 1,
        "displayName": "BOT1_UPDATED",
        "fullName": "Bot One Updated",
        "image": "",
        "localAlias": ""
      },
      "fullPreferences": {
        "timedMessages": {
          "allow": "yes"
        },
        "fullDelete": {
          "allow": "no"
        },
        "reactions": {
          "allow": "yes"
        },
        "voice": {
          "allow": "yes"
        },
        "calls": {
          "allow": "yes"
        }
      },
      "activeUser": true,
      "activeOrder": 4,
      "showNtfs": true,
      "sendRcptsContacts": true,
      "sendRcptsSmallGroups": true,
      "userMemberProfileUpdatedAt": "2025-05-03T08:42:55.098428Z"
    }
  }
}
```

**Response Type:** `activeUser`

Active user information returned (userId: 1, displayName: BOT1_UPDATED).

### Set Profile Address (disable)

**Command:** `/profile_address off`

**Status:** ✅ Success

**Response:**
```json
{
  "corrId": "3",
  "resp": {
    "type": "usersList",
    "users": [
      {
        "user": {
          "userId": 1,
          "agentUserId": "1",
          "userContactId": 1,
          "localDisplayName": "BOT1_UPDATED",
          "profile": {
            "profileId": 1,
            "displayName": "BOT1_UPDATED",
            "fullName": "Bot One Updated",
            "image": "",
            "localAlias": ""
          },
          "fullPreferences": {
            "timedMessages": {
              "allow": "yes"
            },
            "fullDelete": {
              "allow": "no"
            },
            "reactions": {
              "allow": "yes"
            },
            "voice": {
              "allow": "yes"
            },
            "calls": {
              "allow": "yes"
            }
          },
          "activeUser": true,
          "activeOrder": 4,
          "showNtfs": true,
          "sendRcptsContacts": true,
          "sendRcptsSmallGroups": true,
          "userMemberProfileUpdatedAt": "2025-05-03T08:42:55.098428Z"
        },
        "unreadCount": 0
      },
      {
        "user": {
          "userId": 2,
          "agentUserId": "2",
          "userContactId": 5,
          "localDisplayName": "TEST_USER",
          "profile": {
            "profileId": 5,
            "displayName": "TEST_USER",
            "fullName": "Test User",
            "localAlias": ""
          },
          "fullPreferences": {
            "timedMessages": {
              "allow": "yes"
            },
            "fullDelete": {
              "allow": "no"
            },
            "reactions": {
              "allow": "yes"
            },
            "voice": {
              "allow": "yes"
            },
            "calls": {
              "allow": "yes"
            }
          },
          "activeUser": false,
          "activeOrder": 2,
          "showNtfs": true,
          "sendRcptsContacts": true,
          "sendRcptsSmallGroups": true
        },
        "unreadCount": 0
      }
    ]
  }
}
```

**Response Type:** `usersList`

### Address Auto Accept

**Command:** `/auto_accept off`

**Status:** ❌ Error

**Error Message:** Error type: error

**Response:**
```json
{
  "corrId": "4",
  "resp": {
    "type": "chatCmdError",
    "chatError": {
      "type": "error",
      "errorType": {
        "type": "userExists",
        "contactName": "TEST_USER"
      }
    }
  }
}
```

### Show My Address (shorthand)

**Command:** `/sa`

**Status:** ✅ Success

**Response:**
```json
{
  "corrId": "5",
  "resp": {
    "type": "userPrivacy",
    "user": {
      "userId": 1,
      "agentUserId": "1",
      "userContactId": 1,
      "localDisplayName": "BOT1_UPDATED",
      "profile": {
        "profileId": 1,
        "displayName": "BOT1_UPDATED",
        "fullName": "Bot One Updated",
        "image": "",
        "localAlias": ""
      },
      "fullPreferences": {
        "timedMessages": {
          "allow": "yes"
        },
        "fullDelete": {
          "allow": "no"
        },
        "reactions": {
          "allow": "yes"
        },
        "voice": {
          "allow": "yes"
        },
        "calls": {
          "allow": "yes"
        }
      },
      "activeUser": true,
      "activeOrder": 4,
      "viewPwdHash": {
        "hash": "kNnR3XIVQH2u-HV7rv69v5PZ347oyvYYSpMWMkJ7Ph0ppBjcpJJF-MNYw18IU36s5tVrNCrOhoMYUP0F3fXSgg==",
        "salt": "kW5AahHwHb83YIe2zTtwEA=="
      },
      "showNtfs": false,
      "sendRcptsContacts": true,
      "sendRcptsSmallGroups": true,
      "userMemberProfileUpdatedAt": "2025-05-03T08:42:55.098428Z"
    },
    "updatedUser": {
      "userId": 1,
      "agentUserId": "1",
      "userContactId": 1,
      "localDisplayName": "BOT1_UPDATED",
      "profile": {
        "profileId": 1,
        "displayName": "BOT1_UPDATED",
        "fullName": "Bot One Updated",
        "image": "",
        "localAlias": ""
      },
      "fullPreferences": {
        "timedMessages": {
          "allow": "yes"
        },
        "fullDelete": {
          "allow": "no"
        },
        "reactions": {
          "allow": "yes"
        },
        "voice": {
          "allow": "yes"
        },
        "calls": {
          "allow": "yes"
        }
      },
      "activeUser": true,
      "activeOrder": 4,
      "viewPwdHash": {
        "hash": "kNnR3XIVQH2u-HV7rv69v5PZ347oyvYYSpMWMkJ7Ph0ppBjcpJJF-MNYw18IU36s5tVrNCrOhoMYUP0F3fXSgg==",
        "salt": "kW5AahHwHb83YIe2zTtwEA=="
      },
      "showNtfs": false,
      "sendRcptsContacts": true,
      "sendRcptsSmallGroups": true,
      "userMemberProfileUpdatedAt": "2025-05-03T08:42:55.098428Z"
    }
  }
}
```

**Response Type:** `userPrivacy`

### Create My Address (API version)

**Command:** `/_address 1 short=on`

**Status:** ✅ Success

**Response:**
```json
{
  "corrId": "6",
  "resp": {
    "type": "userPrivacy",
    "user": {
      "userId": 1,
      "agentUserId": "1",
      "userContactId": 1,
      "localDisplayName": "BOT1_UPDATED",
      "profile": {
        "profileId": 1,
        "displayName": "BOT1_UPDATED",
        "fullName": "Bot One Updated",
        "image": "",
        "localAlias": ""
      },
      "fullPreferences": {
        "timedMessages": {
          "allow": "yes"
        },
        "fullDelete": {
          "allow": "no"
        },
        "reactions": {
          "allow": "yes"
        },
        "voice": {
          "allow": "yes"
        },
        "calls": {
          "allow": "yes"
        }
      },
      "activeUser": true,
      "activeOrder": 4,
      "showNtfs": true,
      "sendRcptsContacts": true,
      "sendRcptsSmallGroups": true,
      "userMemberProfileUpdatedAt": "2025-05-03T08:42:55.098428Z"
    },
    "updatedUser": {
      "userId": 1,
      "agentUserId": "1",
      "userContactId": 1,
      "localDisplayName": "BOT1_UPDATED",
      "profile": {
        "profileId": 1,
        "displayName": "BOT1_UPDATED",
        "fullName": "Bot One Updated",
        "image": "",
        "localAlias": ""
      },
      "fullPreferences": {
        "timedMessages": {
          "allow": "yes"
        },
        "fullDelete": {
          "allow": "no"
        },
        "reactions": {
          "allow": "yes"
        },
        "voice": {
          "allow": "yes"
        },
        "calls": {
          "allow": "yes"
        }
      },
      "activeUser": true,
      "activeOrder": 4,
      "showNtfs": true,
      "sendRcptsContacts": true,
      "sendRcptsSmallGroups": true,
      "userMemberProfileUpdatedAt": "2025-05-03T08:42:55.098428Z"
    }
  }
}
```

**Response Type:** `userPrivacy`

### Delete My Address

**Command:** `/_delete_address 1`

**Status:** ✅ Success

**Response:**
```json
{
  "corrId": "7",
  "resp": {
    "type": "userPrivacy",
    "user": {
      "userId": 1,
      "agentUserId": "1",
      "userContactId": 1,
      "localDisplayName": "BOT1_UPDATED",
      "profile": {
        "profileId": 1,
        "displayName": "BOT1_UPDATED",
        "fullName": "Bot One Updated",
        "image": "",
        "localAlias": ""
      },
      "fullPreferences": {
        "timedMessages": {
          "allow": "yes"
        },
        "fullDelete": {
          "allow": "no"
        },
        "reactions": {
          "allow": "yes"
        },
        "voice": {
          "allow": "yes"
        },
        "calls": {
          "allow": "yes"
        }
      },
      "activeUser": true,
      "activeOrder": 4,
      "showNtfs": false,
      "sendRcptsContacts": true,
      "sendRcptsSmallGroups": true,
      "userMemberProfileUpdatedAt": "2025-05-03T08:42:55.098428Z"
    },
    "updatedUser": {
      "userId": 1,
      "agentUserId": "1",
      "userContactId": 1,
      "localDisplayName": "BOT1_UPDATED",
      "profile": {
        "profileId": 1,
        "displayName": "BOT1_UPDATED",
        "fullName": "Bot One Updated",
        "image": "",
        "localAlias": ""
      },
      "fullPreferences": {
        "timedMessages": {
          "allow": "yes"
        },
        "fullDelete": {
          "allow": "no"
        },
        "reactions": {
          "allow": "yes"
        },
        "voice": {
          "allow": "yes"
        },
        "calls": {
          "allow": "yes"
        }
      },
      "activeUser": true,
      "activeOrder": 4,
      "showNtfs": false,
      "sendRcptsContacts": true,
      "sendRcptsSmallGroups": true,
      "userMemberProfileUpdatedAt": "2025-05-03T08:42:55.098428Z"
    }
  }
}
```

**Response Type:** `userPrivacy`


## Chat Commands

### Start Chat

**Command:** `/_start subscribe=on expire=on`

**Status:** ✅ Success

**Response:**
```json
{
  "corrId": "8",
  "resp": {
    "type": "userPrivacy",
    "user": {
      "userId": 1,
      "agentUserId": "1",
      "userContactId": 1,
      "localDisplayName": "BOT1_UPDATED",
      "profile": {
        "profileId": 1,
        "displayName": "BOT1_UPDATED",
        "fullName": "Bot One Updated",
        "image": "",
        "localAlias": ""
      },
      "fullPreferences": {
        "timedMessages": {
          "allow": "yes"
        },
        "fullDelete": {
          "allow": "no"
        },
        "reactions": {
          "allow": "yes"
        },
        "voice": {
          "allow": "yes"
        },
        "calls": {
          "allow": "yes"
        }
      },
      "activeUser": true,
      "activeOrder": 4,
      "showNtfs": true,
      "sendRcptsContacts": true,
      "sendRcptsSmallGroups": true,
      "userMemberProfileUpdatedAt": "2025-05-03T08:42:55.098428Z"
    },
    "updatedUser": {
      "userId": 1,
      "agentUserId": "1",
      "userContactId": 1,
      "localDisplayName": "BOT1_UPDATED",
      "profile": {
        "profileId": 1,
        "displayName": "BOT1_UPDATED",
        "fullName": "Bot One Updated",
        "image": "",
        "localAlias": ""
      },
      "fullPreferences": {
        "timedMessages": {
          "allow": "yes"
        },
        "fullDelete": {
          "allow": "no"
        },
        "reactions": {
          "allow": "yes"
        },
        "voice": {
          "allow": "yes"
        },
        "calls": {
          "allow": "yes"
        }
      },
      "activeUser": true,
      "activeOrder": 4,
      "showNtfs": true,
      "sendRcptsContacts": true,
      "sendRcptsSmallGroups": true,
      "userMemberProfileUpdatedAt": "2025-05-03T08:42:55.098428Z"
    }
  }
}
```

**Response Type:** `userPrivacy`

### Get Chats

**Command:** `/chats`

**Status:** ✅ Success

**Response:**
```json
{
  "corrId": "9",
  "resp": {
    "type": "activeUser",
    "user": {
      "userId": 1,
      "agentUserId": "1",
      "userContactId": 1,
      "localDisplayName": "BOT1_UPDATED",
      "profile": {
        "profileId": 1,
        "displayName": "BOT1_UPDATED",
        "fullName": "Bot One Updated",
        "image": "",
        "localAlias": ""
      },
      "fullPreferences": {
        "timedMessages": {
          "allow": "yes"
        },
        "fullDelete": {
          "allow": "no"
        },
        "reactions": {
          "allow": "yes"
        },
        "voice": {
          "allow": "yes"
        },
        "calls": {
          "allow": "yes"
        }
      },
      "activeUser": true,
      "activeOrder": 5,
      "showNtfs": true,
      "sendRcptsContacts": true,
      "sendRcptsSmallGroups": true,
      "userMemberProfileUpdatedAt": "2025-05-03T08:42:55.098428Z"
    }
  }
}
```

**Response Type:** `activeUser`

Active user information returned (userId: 1, displayName: BOT1_UPDATED).


## Group Commands

### Create Group

**Command:** `/group Test API Group Testing SimpleX WebSocket API None`

**Format:** `/group displayName fullName image`

Creates a new group with the specified display name, full name, and image.

**Status:** ✅ Success

**Response:**
```json
{
  "corrId": "10",
  "resp": {
    "type": "userProfileNoChange",
    "user": {
      "userId": 1,
      "agentUserId": "1",
      "userContactId": 1,
      "localDisplayName": "BOT1_UPDATED",
      "profile": {
        "profileId": 1,
        "displayName": "BOT1_UPDATED",
        "fullName": "Bot One Updated",
        "image": "",
        "localAlias": ""
      },
      "fullPreferences": {
        "timedMessages": {
          "allow": "yes"
        },
        "fullDelete": {
          "allow": "no"
        },
        "reactions": {
          "allow": "yes"
        },
        "voice": {
          "allow": "yes"
        },
        "calls": {
          "allow": "yes"
        }
      },
      "activeUser": true,
      "activeOrder": 5,
      "showNtfs": true,
      "sendRcptsContacts": true,
      "sendRcptsSmallGroups": true,
      "userMemberProfileUpdatedAt": "2025-05-03T08:42:55.098428Z"
    }
  }
}
```

**Response Type:** `userProfileNoChange`


## Contact Commands


## Message Commands


## Server Protocol Commands

### Get SMP Servers

**Command:** `/smp`

**Status:** ✅ Success

**Response:**
```json
{
  "corrId": "11",
  "resp": {
    "type": "userContactLinkCreated",
    "user": {
      "userId": 1,
      "agentUserId": "1",
      "userContactId": 1,
      "localDisplayName": "BOT1_UPDATED",
      "profile": {
        "profileId": 1,
        "displayName": "BOT1_UPDATED",
        "fullName": "Bot One Updated",
        "image": "",
        "localAlias": ""
      },
      "fullPreferences": {
        "timedMessages": {
          "allow": "yes"
        },
        "fullDelete": {
          "allow": "no"
        },
        "reactions": {
          "allow": "yes"
        },
        "voice": {
          "allow": "yes"
        },
        "calls": {
          "allow": "yes"
        }
      },
      "activeUser": true,
      "activeOrder": 5,
      "showNtfs": true,
      "sendRcptsContacts": true,
      "sendRcptsSmallGroups": true,
      "userMemberProfileUpdatedAt": "2025-05-03T08:42:55.098428Z"
    },
    "connLinkContact": {
      "connFullLink": "simplex:/contact#/?v=2-7&smp=smp%3A%2F%2Fhpq7_4gGJiilmz5Rf-CswuU5kZGkm_zOIooSw6yALRg%3D%40smp5.simplex.im%2FZ5T-r90Dy9UcHG3otBW_Ol6mKwJM45_O%23%2F%3Fv%3D1-4%26dh%3DMCowBQYDK2VuAyEAHbDlW6MNy7x3BuX_RKGVBcMHFBkGa2XLewtGCx3sJ3E%253D%26q%3Dc%26srv%3Djjbyvoemxysm7qxap7m5d5m35jzv5qq6gnlv7s4rsn7tdwwmuqciwpid.onion"
    }
  }
}
```

**Response Type:** `userContactLinkCreated`

### Get XFTP Servers

**Command:** `/xftp`

**Status:** ✅ Success

**Response:**
```json
{
  "corrId": "12",
  "resp": {
    "type": "userContactLink",
    "user": {
      "userId": 1,
      "agentUserId": "1",
      "userContactId": 1,
      "localDisplayName": "BOT1_UPDATED",
      "profile": {
        "profileId": 1,
        "displayName": "BOT1_UPDATED",
        "fullName": "Bot One Updated",
        "image": "",
        "localAlias": ""
      },
      "fullPreferences": {
        "timedMessages": {
          "allow": "yes"
        },
        "fullDelete": {
          "allow": "no"
        },
        "reactions": {
          "allow": "yes"
        },
        "voice": {
          "allow": "yes"
        },
        "calls": {
          "allow": "yes"
        }
      },
      "activeUser": true,
      "activeOrder": 5,
      "showNtfs": true,
      "sendRcptsContacts": true,
      "sendRcptsSmallGroups": true,
      "userMemberProfileUpdatedAt": "2025-05-03T08:42:55.098428Z"
    },
    "contactLink": {
      "connLinkContact": {
        "connFullLink": "simplex:/contact#/?v=2-7&smp=smp%3A%2F%2Fhpq7_4gGJiilmz5Rf-CswuU5kZGkm_zOIooSw6yALRg%3D%40smp5.simplex.im%2FZ5T-r90Dy9UcHG3otBW_Ol6mKwJM45_O%23%2F%3Fv%3D1-4%26dh%3DMCowBQYDK2VuAyEAHbDlW6MNy7x3BuX_RKGVBcMHFBkGa2XLewtGCx3sJ3E%253D%26q%3Dc%26srv%3Djjbyvoemxysm7qxap7m5d5m35jzv5qq6gnlv7s4rsn7tdwwmuqciwpid.onion"
      }
    }
  }
}
```

**Response Type:** `userContactLink`

User's contact link information returned.

### Test Server

**Command:** `/_server test 1 smp://u2dS9sG8nMNURyZwqASV4yROM28Er0luVTx5X1CsMrU=@smp4.simplex.im`

**Status:** ✅ Success

**Response:**
```json
{
  "corrId": "13",
  "resp": {
    "type": "userProfileUpdated",
    "user": {
      "userId": 1,
      "agentUserId": "1",
      "userContactId": 1,
      "localDisplayName": "BOT1_UPDATED",
      "profile": {
        "profileId": 1,
        "displayName": "BOT1_UPDATED",
        "fullName": "Bot One Updated",
        "image": "",
        "contactLink": "simplex:/contact#/?v=2-7&smp=smp%3A%2F%2Fhpq7_4gGJiilmz5Rf-CswuU5kZGkm_zOIooSw6yALRg%3D%40smp5.simplex.im%2FZ5T-r90Dy9UcHG3otBW_Ol6mKwJM45_O%23%2F%3Fv%3D1-4%26dh%3DMCowBQYDK2VuAyEAHbDlW6MNy7x3BuX_RKGVBcMHFBkGa2XLewtGCx3sJ3E%253D%26q%3Dc%26srv%3Djjbyvoemxysm7qxap7m5d5m35jzv5qq6gnlv7s4rsn7tdwwmuqciwpid.onion",
        "localAlias": ""
      },
      "fullPreferences": {
        "timedMessages": {
          "allow": "yes"
        },
        "fullDelete": {
          "allow": "no"
        },
        "reactions": {
          "allow": "yes"
        },
        "voice": {
          "allow": "yes"
        },
        "calls": {
          "allow": "yes"
        }
      },
      "activeUser": true,
      "activeOrder": 5,
      "showNtfs": true,
      "sendRcptsContacts": true,
      "sendRcptsSmallGroups": true,
      "userMemberProfileUpdatedAt": "2025-05-03T08:42:55.098428Z"
    },
    "fromProfile": {
      "displayName": "BOT1_UPDATED",
      "fullName": "Bot One Updated",
      "image": ""
    },
    "toProfile": {
      "displayName": "BOT1_UPDATED",
      "fullName": "Bot One Updated",
      "image": "",
      "contactLink": "simplex:/contact#/?v=2-7&smp=smp%3A%2F%2Fhpq7_4gGJiilmz5Rf-CswuU5kZGkm_zOIooSw6yALRg%3D%40smp5.simplex.im%2FZ5T-r90Dy9UcHG3otBW_Ol6mKwJM45_O%23%2F%3Fv%3D1-4%26dh%3DMCowBQYDK2VuAyEAHbDlW6MNy7x3BuX_RKGVBcMHFBkGa2XLewtGCx3sJ3E%253D%26q%3Dc%26srv%3Djjbyvoemxysm7qxap7m5d5m35jzv5qq6gnlv7s4rsn7tdwwmuqciwpid.onion"
    },
    "updateSummary": {
      "updateSuccesses": 1,
      "updateFailures": 0,
      "changedContacts": []
    }
  }
}
```

**Response Type:** `userProfileUpdated`

### Get User Servers

**Command:** `/_servers 1`

**Status:** ✅ Success

**Response:**
```json
{
  "resp": {
    "type": "newChatItems",
    "user": {
      "userId": 1,
      "agentUserId": "1",
      "userContactId": 1,
      "localDisplayName": "BOT1_UPDATED",
      "profile": {
        "profileId": 1,
        "displayName": "BOT1_UPDATED",
        "fullName": "Bot One Updated",
        "image": "",
        "contactLink": "simplex:/contact#/?v=2-7&smp=smp%3A%2F%2Fhpq7_4gGJiilmz5Rf-CswuU5kZGkm_zOIooSw6yALRg%3D%40smp5.simplex.im%2FZ5T-r90Dy9UcHG3otBW_Ol6mKwJM45_O%23%2F%3Fv%3D1-4%26dh%3DMCowBQYDK2VuAyEAHbDlW6MNy7x3BuX_RKGVBcMHFBkGa2XLewtGCx3sJ3E%253D%26q%3Dc%26srv%3Djjbyvoemxysm7qxap7m5d5m35jzv5qq6gnlv7s4rsn7tdwwmuqciwpid.onion",
        "localAlias": ""
      },
      "fullPreferences": {
        "timedMessages": {
          "allow": "yes"
        },
        "fullDelete": {
          "allow": "no"
        },
        "reactions": {
          "allow": "yes"
        },
        "voice": {
          "allow": "yes"
        },
        "calls": {
          "allow": "yes"
        }
      },
      "activeUser": true,
      "activeOrder": 5,
      "showNtfs": true,
      "sendRcptsContacts": true,
      "sendRcptsSmallGroups": true,
      "userMemberProfileUpdatedAt": "2025-05-03T08:42:55.098428Z"
    },
    "chatItems": []
  }
}
```

**Response Type:** `newChatItems`


## Database Commands


## File Commands

### Set Temp Folder

**Command:** `/_temp_folder /tmp/simplex_test`

**Status:** ✅ Success

**Response:**
```json
{
  "corrId": "14",
  "resp": {
    "type": "userProfileUpdated",
    "user": {
      "userId": 1,
      "agentUserId": "1",
      "userContactId": 1,
      "localDisplayName": "BOT1_UPDATED",
      "profile": {
        "profileId": 1,
        "displayName": "BOT1_UPDATED",
        "fullName": "Bot One Updated",
        "image": "",
        "localAlias": ""
      },
      "fullPreferences": {
        "timedMessages": {
          "allow": "yes"
        },
        "fullDelete": {
          "allow": "no"
        },
        "reactions": {
          "allow": "yes"
        },
        "voice": {
          "allow": "yes"
        },
        "calls": {
          "allow": "yes"
        }
      },
      "activeUser": true,
      "activeOrder": 5,
      "showNtfs": true,
      "sendRcptsContacts": true,
      "sendRcptsSmallGroups": true,
      "userMemberProfileUpdatedAt": "2025-05-03T08:42:55.098428Z"
    },
    "fromProfile": {
      "displayName": "BOT1_UPDATED",
      "fullName": "Bot One Updated",
      "image": "",
      "contactLink": "simplex:/contact#/?v=2-7&smp=smp%3A%2F%2Fhpq7_4gGJiilmz5Rf-CswuU5kZGkm_zOIooSw6yALRg%3D%40smp5.simplex.im%2FZ5T-r90Dy9UcHG3otBW_Ol6mKwJM45_O%23%2F%3Fv%3D1-4%26dh%3DMCowBQYDK2VuAyEAHbDlW6MNy7x3BuX_RKGVBcMHFBkGa2XLewtGCx3sJ3E%253D%26q%3Dc%26srv%3Djjbyvoemxysm7qxap7m5d5m35jzv5qq6gnlv7s4rsn7tdwwmuqciwpid.onion"
    },
    "toProfile": {
      "displayName": "BOT1_UPDATED",
      "fullName": "Bot One Updated",
      "image": ""
    },
    "updateSummary": {
      "updateSuccesses": 1,
      "updateFailures": 0,
      "changedContacts": []
    }
  }
}
```

**Response Type:** `userProfileUpdated`

### Set Files Folder

**Command:** `/_files_folder /tmp/simplex_test`

**Status:** ✅ Success

**Response:**
```json
{
  "resp": {
    "type": "newChatItems",
    "user": {
      "userId": 1,
      "agentUserId": "1",
      "userContactId": 1,
      "localDisplayName": "BOT1_UPDATED",
      "profile": {
        "profileId": 1,
        "displayName": "BOT1_UPDATED",
        "fullName": "Bot One Updated",
        "image": "",
        "localAlias": ""
      },
      "fullPreferences": {
        "timedMessages": {
          "allow": "yes"
        },
        "fullDelete": {
          "allow": "no"
        },
        "reactions": {
          "allow": "yes"
        },
        "voice": {
          "allow": "yes"
        },
        "calls": {
          "allow": "yes"
        }
      },
      "activeUser": true,
      "activeOrder": 5,
      "showNtfs": true,
      "sendRcptsContacts": true,
      "sendRcptsSmallGroups": true,
      "userMemberProfileUpdatedAt": "2025-05-03T08:42:55.098428Z"
    },
    "chatItems": []
  }
}
```

**Response Type:** `newChatItems`

### Set Incognito Mode

**Command:** `/incognito on`

**Status:** ✅ Success

**Response:**
```json
{
  "corrId": "15",
  "resp": {
    "type": "userContactLinkUpdated",
    "user": {
      "userId": 1,
      "agentUserId": "1",
      "userContactId": 1,
      "localDisplayName": "BOT1_UPDATED",
      "profile": {
        "profileId": 1,
        "displayName": "BOT1_UPDATED",
        "fullName": "Bot One Updated",
        "image": "",
        "localAlias": ""
      },
      "fullPreferences": {
        "timedMessages": {
          "allow": "yes"
        },
        "fullDelete": {
          "allow": "no"
        },
        "reactions": {
          "allow": "yes"
        },
        "voice": {
          "allow": "yes"
        },
        "calls": {
          "allow": "yes"
        }
      },
      "activeUser": true,
      "activeOrder": 5,
      "showNtfs": true,
      "sendRcptsContacts": true,
      "sendRcptsSmallGroups": true,
      "userMemberProfileUpdatedAt": "2025-05-03T08:42:55.098428Z"
    },
    "contactLink": {
      "connLinkContact": {
        "connFullLink": "simplex:/contact#/?v=2-7&smp=smp%3A%2F%2Fhpq7_4gGJiilmz5Rf-CswuU5kZGkm_zOIooSw6yALRg%3D%40smp5.simplex.im%2FZ5T-r90Dy9UcHG3otBW_Ol6mKwJM45_O%23%2F%3Fv%3D1-4%26dh%3DMCowBQYDK2VuAyEAHbDlW6MNy7x3BuX_RKGVBcMHFBkGa2XLewtGCx3sJ3E%253D%26q%3Dc%26srv%3Djjbyvoemxysm7qxap7m5d5m35jzv5qq6gnlv7s4rsn7tdwwmuqciwpid.onion"
      }
    }
  }
}
```

**Response Type:** `userContactLinkUpdated`

### Disable Incognito Mode

**Command:** `/incognito off`

**Status:** ✅ Success

**Response:**
```json
{
  "corrId": "16",
  "resp": {
    "type": "userContactLink",
    "user": {
      "userId": 1,
      "agentUserId": "1",
      "userContactId": 1,
      "localDisplayName": "BOT1_UPDATED",
      "profile": {
        "profileId": 1,
        "displayName": "BOT1_UPDATED",
        "fullName": "Bot One Updated",
        "image": "",
        "localAlias": ""
      },
      "fullPreferences": {
        "timedMessages": {
          "allow": "yes"
        },
        "fullDelete": {
          "allow": "no"
        },
        "reactions": {
          "allow": "yes"
        },
        "voice": {
          "allow": "yes"
        },
        "calls": {
          "allow": "yes"
        }
      },
      "activeUser": true,
      "activeOrder": 5,
      "showNtfs": true,
      "sendRcptsContacts": true,
      "sendRcptsSmallGroups": true,
      "userMemberProfileUpdatedAt": "2025-05-03T08:42:55.098428Z"
    },
    "contactLink": {
      "connLinkContact": {
        "connFullLink": "simplex:/contact#/?v=2-7&smp=smp%3A%2F%2Fhpq7_4gGJiilmz5Rf-CswuU5kZGkm_zOIooSw6yALRg%3D%40smp5.simplex.im%2FZ5T-r90Dy9UcHG3otBW_Ol6mKwJM45_O%23%2F%3Fv%3D1-4%26dh%3DMCowBQYDK2VuAyEAHbDlW6MNy7x3BuX_RKGVBcMHFBkGa2XLewtGCx3sJ3E%253D%26q%3Dc%26srv%3Djjbyvoemxysm7qxap7m5d5m35jzv5qq6gnlv7s4rsn7tdwwmuqciwpid.onion"
      }
    }
  }
}
```

**Response Type:** `userContactLink`

User's contact link information returned.


## Miscellaneous Commands

### Show Version

**Command:** `/version`

**Status:** ❌ Error

**Error Message:** Error type: error

**Response:**
```json
{
  "corrId": "19",
  "resp": {
    "type": "chatCmdError",
    "chatError": {
      "type": "error",
      "errorType": {
        "type": "commandError",
        "message": "Failed reading: empty"
      }
    }
  }
}
```

### Check Chat Running

**Command:** `/_check running`

**Status:** ❌ Error

**Error Message:** Error type: errorStore

**Response:**
```json
{
  "corrId": "17",
  "resp": {
    "type": "chatCmdError",
    "user_": {
      "userId": 1,
      "agentUserId": "1",
      "userContactId": 1,
      "localDisplayName": "BOT1_UPDATED",
      "profile": {
        "profileId": 1,
        "displayName": "BOT1_UPDATED",
        "fullName": "Bot One Updated",
        "image": "",
        "localAlias": ""
      },
      "fullPreferences": {
        "timedMessages": {
          "allow": "yes"
        },
        "fullDelete": {
          "allow": "no"
        },
        "reactions": {
          "allow": "yes"
        },
        "voice": {
          "allow": "yes"
        },
        "calls": {
          "allow": "yes"
        }
      },
      "activeUser": true,
      "activeOrder": 5,
      "showNtfs": true,
      "sendRcptsContacts": true,
      "sendRcptsSmallGroups": true,
      "userMemberProfileUpdatedAt": "2025-05-03T08:42:55.098428Z"
    },
    "chatError": {
      "type": "errorStore",
      "storeError": {
        "type": "duplicateContactLink"
      }
    }
  }
}
```

### Get Network Config

**Command:** `/network`

**Status:** ✅ Success

**Response:**
```json
{
  "corrId": "18",
  "resp": {
    "type": "userContactLinkDeleted",
    "user": {
      "userId": 1,
      "agentUserId": "1",
      "userContactId": 1,
      "localDisplayName": "BOT1_UPDATED",
      "profile": {
        "profileId": 1,
        "displayName": "BOT1_UPDATED",
        "fullName": "Bot One Updated",
        "image": "",
        "localAlias": ""
      },
      "fullPreferences": {
        "timedMessages": {
          "allow": "yes"
        },
        "fullDelete": {
          "allow": "no"
        },
        "reactions": {
          "allow": "yes"
        },
        "voice": {
          "allow": "yes"
        },
        "calls": {
          "allow": "yes"
        }
      },
      "activeUser": true,
      "activeOrder": 5,
      "showNtfs": true,
      "sendRcptsContacts": true,
      "sendRcptsSmallGroups": true,
      "userMemberProfileUpdatedAt": "2025-05-03T08:42:55.098428Z"
    }
  }
}
```

**Response Type:** `userContactLinkDeleted`

### Get Network Statuses

**Command:** `/_network_statuses`

**Status:** ✅ Success

**Response:**
```json
{
  "corrId": "20",
  "resp": {
    "type": "chats",
    "chats": [
      {
        "chatInfo": {
          "type": "direct",
          "contact": {
            "contactId": 4,
            "localDisplayName": "BOT2",
            "profile": {
              "profileId": 4,
              "displayName": "BOT2",
              "fullName": "",
              "preferences": {
                "timedMessages": {
                  "allow": "yes"
                },
                "fullDelete": {
                  "allow": "no"
                },
                "reactions": {
                  "allow": "yes"
                },
                "voice": {
                  "allow": "yes"
                },
                "calls": {
                  "allow": "yes"
                }
              },
              "localAlias": "BOT2_ALIAS"
            },
            "activeConn": {
              "connId": 2,
              "agentConnId": "MjhOZUlmVEFjSVBxR0VqQQ==",
              "connChatVersion": 14,
              "peerChatVRange": {
                "minVersion": 1,
                "maxVersion": 14
              },
              "connLevel": 0,
              "viaGroupLink": false,
              "connType": "contact",
              "connStatus": "ready",
              "contactConnInitiated": false,
              "localAlias": "",
              "entityId": 4,
              "pqSupport": true,
              "pqEncryption": true,
              "pqSndEnabled": true,
              "pqRcvEnabled": true,
              "authErrCounter": 0,
              "quotaErrCounter": 0,
              "createdAt": "2025-05-03T08:15:38.727032Z"
            },
            "contactUsed": true,
            "contactStatus": "active",
            "chatSettings": {
              "enableNtfs": "all",
              "favorite": false
            },
            "userPreferences": {},
            "mergedPreferences": {
              "timedMessages": {
                "enabled": {
                  "forUser": true,
                  "forContact": true
                },
                "userPreference": {
                  "type": "user",
                  "preference": {
                    "allow": "yes"
                  }
                },
                "contactPreference": {
                  "allow": "yes"
                }
              },
              "fullDelete": {
                "enabled": {
                  "forUser": false,
                  "forContact": false
                },
                "userPreference": {
                  "type": "user",
                  "preference": {
                    "allow": "no"
                  }
                },
                "contactPreference": {
                  "allow": "no"
                }
              },
              "reactions": {
                "enabled": {
                  "forUser": true,
                  "forContact": true
                },
                "userPreference": {
                  "type": "user",
                  "preference": {
                    "allow": "yes"
                  }
                },
                "contactPreference": {
                  "allow": "yes"
                }
              },
              "voice": {
                "enabled": {
                  "forUser": true,
                  "forContact": true
                },
                "userPreference": {
                  "type": "user",
                  "preference": {
                    "allow": "yes"
                  }
                },
                "contactPreference": {
                  "allow": "yes"
                }
              },
              "calls": {
                "enabled": {
                  "forUser": true,
                  "forContact": true
                },
                "userPreference": {
                  "type": "user",
                  "preference": {
                    "allow": "yes"
                  }
                },
                "contactPreference": {
                  "allow": "yes"
                }
              }
            },
            "createdAt": "2025-05-03T08:15:38.727032Z",
            "updatedAt": "2025-05-03T08:15:38.727032Z",
            "chatTs": "2025-05-03T08:53:01.343616Z",
            "contactGrpInvSent": false,
            "chatTags": [],
            "chatDeleted": false
          }
        },
        "chatItems": [
          {
            "chatDir": {
              "type": "directSnd"
            },
            "meta": {
              "itemId": 45,
              "itemTs": "2025-05-03T08:53:01.343616Z",
              "itemText": "# Heading\n**Bold text** and *italic text*\n```\ncode block\n```",
              "itemStatus": {
                "type": "sndRcvd",
                "msgRcptStatus": "ok",
                "sndProgress": "complete"
              },
              "sentViaProxy": false,
              "itemSharedMsgId": "d1NPUHVDSDAyVWVTNnVwUA==",
              "itemEdited": false,
              "userMention": false,
              "deletable": true,
              "editable": true,
              "createdAt": "2025-05-03T08:53:01.343616Z",
              "updatedAt": "2025-05-03T08:53:02.731548Z"
            },
            "content": {
              "type": "sndMsgContent",
              "msgContent": {
                "type": "text",
                "text": "# Heading\n**Bold text** and *italic text*\n```\ncode block\n```"
              }
            },
            "mentions": {},
            "formattedText": [
              {
                "text": "# Heading\n**Bold text** and "
              },
              {
                "format": {
                  "type": "bold"
                },
                "text": "italic text"
              },
              {
                "text": "\n```\ncode block\n```"
              }
            ],
            "reactions": []
          }
        ],
        "chatStats": {
          "unreadCount": 0,
          "unreadMentions": 0,
          "reportsCount": 0,
          "minUnreadItemId": 0,
          "unreadChat": false
        }
      },
      {
        "chatInfo": {
          "type": "group",
          "groupInfo": {
            "groupId": 3,
            "localDisplayName": "Test_2",
            "groupProfile": {
              "displayName": "Test",
              "fullName": "API Group Testing SimpleX WebSocket API None",
              "groupPreferences": {
                "directMessages": {
                  "enable": "on"
                },
                "history": {
                  "enable": "on"
                }
              }
            },
            "localAlias": "",
            "fullGroupPreferences": {
              "timedMessages": {
                "enable": "off",
                "ttl": 86400
              },
              "directMessages": {
                "enable": "on"
              },
              "fullDelete": {
                "enable": "off"
              },
              "reactions": {
                "enable": "on"
              },
              "voice": {
                "enable": "on"
              },
              "files": {
                "enable": "on"
              },
              "simplexLinks": {
                "enable": "on"
              },
              "reports": {
                "enable": "on"
              },
              "history": {
                "enable": "on"
              }
            },
            "membership": {
              "groupMemberId": 3,
              "groupId": 3,
              "memberId": "aExGdWRkQWNFa0hnTmhIZw==",
              "memberRole": "owner",
              "memberCategory": "user",
              "memberStatus": "creator",
              "memberSettings": {
                "showMessages": true
              },
              "blockedByAdmin": false,
              "invitedBy": {
                "type": "user"
              },
              "localDisplayName": "BOT1_UPDATED",
              "memberProfile": {
                "profileId": 1,
                "displayName": "BOT1_UPDATED",
                "fullName": "Bot One Updated",
                "image": "",
                "localAlias": ""
              },
              "memberContactId": 1,
              "memberContactProfileId": 1,
              "memberChatVRange": {
                "minVersion": 1,
                "maxVersion": 14
              },
              "createdAt": "2025-05-03T08:53:01.137225Z",
              "updatedAt": "2025-05-03T08:53:01.137225Z"
            },
            "chatSettings": {
              "enableNtfs": "all",
              "favorite": false
            },
            "createdAt": "2025-05-03T08:53:01.137225Z",
            "updatedAt": "2025-05-03T08:53:01.137225Z",
            "chatTs": "2025-05-03T08:53:01.162927Z",
            "userMemberProfileSentAt": "2025-05-03T08:53:01.137225Z",
            "chatTags": []
          }
        },
        "chatItems": [
          {
            "chatDir": {
              "type": "groupSnd"
            },
            "meta": {
              "itemId": 41,
              "itemTs": "2025-05-03T08:53:01.162927Z",
              "itemText": "Recent history: on",
              "itemStatus": {
                "type": "sndNew"
              },
              "itemEdited": false,
              "userMention": false,
              "deletable": false,
              "editable": false,
              "createdAt": "2025-05-03T08:53:01.162927Z",
              "updatedAt": "2025-05-03T08:53:01.162927Z"
            },
            "content": {
              "type": "sndGroupFeature",
              "groupFeature": "history",
              "preference": {
                "enable": "on"
              }
            },
            "mentions": {},
            "reactions": []
          }
        ],
        "chatStats": {
          "unreadCount": 0,
          "unreadMentions": 0,
          "reportsCount": 0,
          "minUnreadItemId": 0,
          "unreadChat": false
        }
      },
      {
        "chatInfo": {
          "type": "group",
          "groupInfo": {
            "groupId": 2,
            "localDisplayName": "Test_1",
            "groupProfile": {
              "displayName": "Test",
              "fullName": "API Group Testing SimpleX WebSocket API None",
              "groupPreferences": {
                "directMessages": {
                  "enable": "on"
                },
                "history": {
                  "enable": "on"
                }
              }
            },
            "localAlias": "",
            "fullGroupPreferences": {
              "timedMessages": {
                "enable": "off",
                "ttl": 86400
              },
              "directMessages": {
                "enable": "on"
              },
              "fullDelete": {
                "enable": "off"
              },
              "reactions": {
                "enable": "on"
              },
              "voice": {
                "enable": "on"
              },
              "files": {
                "enable": "on"
              },
              "simplexLinks": {
                "enable": "on"
              },
              "reports": {
                "enable": "on"
              },
              "history": {
                "enable": "on"
              }
            },
            "membership": {
              "groupMemberId": 2,
              "groupId": 2,
              "memberId": "bTBDdEJOUzJ4NTRNTTBTag==",
              "memberRole": "owner",
              "memberCategory": "user",
              "memberStatus": "creator",
              "memberSettings": {
                "showMessages": true
              },
              "blockedByAdmin": false,
              "invitedBy": {
                "type": "user"
              },
              "localDisplayName": "BOT1_UPDATED",
              "memberProfile": {
                "profileId": 1,
                "displayName": "BOT1_UPDATED",
                "fullName": "Bot One Updated",
                "image": "",
                "localAlias": ""
              },
              "memberContactId": 1,
              "memberContactProfileId": 1,
              "memberChatVRange": {
                "minVersion": 1,
                "maxVersion": 14
              },
              "createdAt": "2025-05-03T08:42:55.93582Z",
              "updatedAt": "2025-05-03T08:42:55.93582Z"
            },
            "chatSettings": {
              "enableNtfs": "all",
              "favorite": false
            },
            "createdAt": "2025-05-03T08:42:55.93582Z",
            "updatedAt": "2025-05-03T08:42:55.93582Z",
            "chatTs": "2025-05-03T08:42:55.956836Z",
            "userMemberProfileSentAt": "2025-05-03T08:42:55.93582Z",
            "chatTags": []
          }
        },
        "chatItems": [
          {
            "chatDir": {
              "type": "groupSnd"
            },
            "meta": {
              "itemId": 26,
              "itemTs": "2025-05-03T08:42:55.956836Z",
              "itemText": "Recent history: on",
              "itemStatus": {
                "type": "sndNew"
              },
              "itemEdited": false,
              "userMention": false,
              "deletable": false,
              "editable": false,
              "createdAt": "2025-05-03T08:42:55.956836Z",
              "updatedAt": "2025-05-03T08:42:55.956836Z"
            },
            "content": {
              "type": "sndGroupFeature",
              "groupFeature": "history",
              "preference": {
                "enable": "on"
              }
            },
            "mentions": {},
            "reactions": []
          }
        ],
        "chatStats": {
          "unreadCount": 0,
          "unreadMentions": 0,
          "reportsCount": 0,
          "minUnreadItemId": 0,
          "unreadChat": false
        }
      },
      {
        "chatInfo": {
          "type": "group",
          "groupInfo": {
            "groupId": 1,
            "localDisplayName": "Test",
            "groupProfile": {
              "displayName": "Test",
              "fullName": "Group Task-21 Test Group for Integration Tests None",
              "groupPreferences": {
                "directMessages": {
                  "enable": "on"
                },
                "history": {
                  "enable": "on"
                }
              }
            },
            "localAlias": "",
            "fullGroupPreferences": {
              "timedMessages": {
                "enable": "off",
                "ttl": 86400
              },
              "directMessages": {
                "enable": "on"
              },
              "fullDelete": {
                "enable": "off"
              },
              "reactions": {
                "enable": "on"
              },
              "voice": {
                "enable": "on"
              },
              "files": {
                "enable": "on"
              },
              "simplexLinks": {
                "enable": "on"
              },
              "reports": {
                "enable": "on"
              },
              "history": {
                "enable": "on"
              }
            },
            "membership": {
              "groupMemberId": 1,
              "groupId": 1,
              "memberId": "Ly9qeW1VU1AzVUw1OWpKag==",
              "memberRole": "owner",
              "memberCategory": "user",
              "memberStatus": "creator",
              "memberSettings": {
                "showMessages": true
              },
              "blockedByAdmin": false,
              "invitedBy": {
                "type": "user"
              },
              "localDisplayName": "BOT1_UPDATED",
              "memberProfile": {
                "profileId": 1,
                "displayName": "BOT1_UPDATED",
                "fullName": "Bot One Updated",
                "image": "",
                "localAlias": ""
              },
              "memberContactId": 1,
              "memberContactProfileId": 1,
              "memberChatVRange": {
                "minVersion": 1,
                "maxVersion": 14
              },
              "createdAt": "2025-05-03T08:36:07.479887Z",
              "updatedAt": "2025-05-03T08:42:55.098428Z"
            },
            "chatSettings": {
              "enableNtfs": "all",
              "favorite": false
            },
            "createdAt": "2025-05-03T08:36:07.479887Z",
            "updatedAt": "2025-05-03T08:36:07.479887Z",
            "chatTs": "2025-05-03T08:36:07.508595Z",
            "userMemberProfileSentAt": "2025-05-03T08:36:07.479887Z",
            "chatTags": []
          }
        },
        "chatItems": [
          {
            "chatDir": {
              "type": "groupSnd"
            },
            "meta": {
              "itemId": 16,
              "itemTs": "2025-05-03T08:36:07.508595Z",
              "itemText": "Recent history: on",
              "itemStatus": {
                "type": "sndNew"
              },
              "itemEdited": false,
              "userMention": false,
              "deletable": false,
              "editable": false,
              "createdAt": "2025-05-03T08:36:07.508595Z",
              "updatedAt": "2025-05-03T08:36:07.508595Z"
            },
            "content": {
              "type": "sndGroupFeature",
              "groupFeature": "history",
              "preference": {
                "enable": "on"
              }
            },
            "mentions": {},
            "reactions": []
          }
        ],
        "chatStats": {
          "unreadCount": 0,
          "unreadMentions": 0,
          "reportsCount": 0,
          "minUnreadItemId": 0,
          "unreadChat": false
        }
      },
      {
        "chatInfo": {
          "type": "direct",
          "contact": {
            "contactId": 3,
            "localDisplayName": "SimpleX Chat team",
            "profile": {
              "profileId": 3,
              "displayName": "SimpleX Chat team",
              "fullName": "",
              "image": "data:image/jpg;base64,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",
              "contactLink": "simplex:/contact#/?v=2&smp=smp%3A%2F%2FPQUV2eL0t7OStZOoAsPEV2QYWt4-xilbakvGUGOItUo%3D%40smp6.simplex.im%2FK1rslx-m5bpXVIdMZg9NLUZ_8JBm8xTt%23%2F%3Fv%3D1%26dh%3DMCowBQYDK2VuAyEALDeVe-sG8mRY22LsXlPgiwTNs9dbiLrNuA7f3ZMAJ2w%253D%26srv%3Dbylepyau3ty4czmn77q4fglvperknl4bi2eb2fdy2bh4jxtf32kf73yd.onion",
              "localAlias": ""
            },
            "contactUsed": true,
            "contactStatus": "active",
            "chatSettings": {
              "enableNtfs": "all",
              "favorite": false
            },
            "userPreferences": {},
            "mergedPreferences": {
              "timedMessages": {
                "enabled": {
                  "forUser": true,
                  "forContact": true
                },
                "userPreference": {
                  "type": "user",
                  "preference": {
                    "allow": "yes"
                  }
                },
                "contactPreference": {
                  "allow": "yes"
                }
              },
              "fullDelete": {
                "enabled": {
                  "forUser": false,
                  "forContact": false
                },
                "userPreference": {
                  "type": "user",
                  "preference": {
                    "allow": "no"
                  }
                },
                "contactPreference": {
                  "allow": "no"
                }
              },
              "reactions": {
                "enabled": {
                  "forUser": true,
                  "forContact": true
                },
                "userPreference": {
                  "type": "user",
                  "preference": {
                    "allow": "yes"
                  }
                },
                "contactPreference": {
                  "allow": "yes"
                }
              },
              "voice": {
                "enabled": {
                  "forUser": true,
                  "forContact": true
                },
                "userPreference": {
                  "type": "user",
                  "preference": {
                    "allow": "yes"
                  }
                },
                "contactPreference": {
                  "allow": "yes"
                }
              },
              "calls": {
                "enabled": {
                  "forUser": true,
                  "forContact": true
                },
                "userPreference": {
                  "type": "user",
                  "preference": {
                    "allow": "yes"
                  }
                },
                "contactPreference": {
                  "allow": "yes"
                }
              }
            },
            "createdAt": "2025-05-03T08:13:55.288057Z",
            "updatedAt": "2025-05-03T08:13:55.288057Z",
            "chatTs": "2025-05-03T08:13:55.288057Z",
            "contactGrpInvSent": false,
            "chatTags": [],
            "chatDeleted": false
          }
        },
        "chatItems": [],
        "chatStats": {
          "unreadCount": 0,
          "unreadMentions": 0,
          "reportsCount": 0,
          "minUnreadItemId": 0,
          "unreadChat": false
        }
      },
      {
        "chatInfo": {
          "type": "direct",
          "contact": {
            "contactId": 2,
            "localDisplayName": "SimpleX-Status",
            "profile": {
              "profileId": 2,
              "displayName": "SimpleX-Status",
              "fullName": "",
              "image": "data:image/jpg;base64,/9j/4AAQSkZJRgABAQAASABIAAD/4QBYRXhpZgAATU0AKgAAAAgAAgESAAMAAAABAAEAAIdpAAQAAAABAAAAJgAAAAAAA6ABAAMAAAABAAEAAKACAAQAAAABAAAAr6ADAAQAAAABAAAArwAAAAD/7QA4UGhvdG9zaG9wIDMuMAA4QklNBAQAAAAAAAA4QklNBCUAAAAAABDUHYzZjwCyBOmACZjs+EJ+/8AAEQgArwCvAwEiAAIRAQMRAf/EAB8AAAEFAQEBAQEBAAAAAAAAAAABAgMEBQYHCAkKC//EALUQAAIBAwMCBAMFBQQEAAABfQECAwAEEQUSITFBBhNRYQcicRQygZGhCCNCscEVUtHwJDNicoIJChYXGBkaJSYnKCkqNDU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6g4SFhoeIiYqSk5SVlpeYmZqio6Slpqeoqaqys7S1tre4ubrCw8TFxsfIycrS09TV1tfY2drh4uPk5ebn6Onq8fLz9PX29/j5+v/EAB8BAAMBAQEBAQEBAQEAAAAAAAABAgMEBQYHCAkKC//EALURAAIBAgQEAwQHBQQEAAECdwABAgMRBAUhMQYSQVEHYXETIjKBCBRCkaGxwQkjM1LwFWJy0QoWJDThJfEXGBkaJicoKSo1Njc4OTpDREVGR0hJSlNUVVZXWFlaY2RlZmdoaWpzdHV2d3h5eoKDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uLj5OXm5+jp6vLz9PX29/j5+v/bAEMAAQEBAQEBAgEBAgMCAgIDBAMDAwMEBgQEBAQEBgcGBgYGBgYHBwcHBwcHBwgICAgICAkJCQkJCwsLCwsLCwsLC//bAEMBAgICAwMDBQMDBQsIBggLCwsLCwsLCwsLCwsLCwsLCwsLCwsLCwsLCwsLCwsLCwsLCwsLCwsLCwsLCwsLCwsLC//dAAQAC//aAAwDAQACEQMRAD8A/v4ooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKAP/Q/v4ooooAKKKKACiiigAoorE8R+ItF8J6Jc+IvEVwlrZ2iGSWWQ4CgVUISlJRirtmdatTo05VaslGMU223ZJLVtvokbdFfl3of/BRbS734rtpup2Ig8LSsIYrjnzkOcea3bafTqBX6cafqFjq1jFqemSrPbzqHjkQ5VlPIINetm2Q43LXD65T5eZXX+XquqPiuC/Efh/itYh5HiVUdGTjJWaflJJ6uEvsy2fqXKKKK8c+5Ciq17e2mnWkl/fyLDDCpd3c4VVHJJJr8c/2kf8Ago34q8M3mpTfByG3fT7CGSJZrlC3nStwJF5GFU8gd69LA5VicXTrVaMfdpxcpPokk397toj4LjvxKyLhGjRqZxValVkowhFc05O9m0tPdjfV7dN2kfq346+J3w9+GWlPrXxA1m00i1QZL3Uqxj8Mnn8K/Mj4tf8ABYD4DeEJ5dM+Gmn3niq4TIE0YEFtn/ffBI+imv51vHfxA8b/ABR1+bxT8RNUuNXvp3LtJcOWCk84VeigdgBXI18LXzupLSkrL72fzrxH9IXNsTKVPKKMaMOkpe/P8fdXpaXqfqvrf/BYH9p6+1w3+iafo1jZA8WrRPKSPeTcpz9BX1l8J/8Ags34PvxDp/xn8M3OmSnAe709hcQfUoSHA/A1/PtSE4/GuKGZ4mLvz39T4TL/ABe4swlZ1ljpTvvGaUo/dbT/ALdsf2rfCX9pT4HfHGzF18M/EdnqTYBaFXCzJn+9G2GH5V7nX8IOm6hqGkX8eraLcy2d3EcpPbuY5FPsykGv6gf+CWf7QPxB+OPwX1Ky+JF22pX3h69+yJdyf62WJlDrvPdlzjPevdwGae3l7OcbP8D+i/DTxm/1ixkcqx2H5K7TalF3jLlV2rPWLtqtWvM/T2iiivYP3c//0f7+KKKKACiiigAooooAK/Fv/goX8Qvi2fFcXgfWrRtP8NDEls0bZS7YfxORxlT0Xt1r9pK8u+L/AMI/Cfxp8F3HgvxbFujlGYpgB5kMg6Op9R+tfR8K5vQy3MYYnE01KK0843+0vNf8NZn5f4wcFZhxTwziMpy3FOjVeqSdo1Lf8u5u11GXk97Xuro/mBFyDX3t+yL+2Be/CW+h8B+OHafw7cyALIxJa0Ldx6p6jt1FfMvx/wDgR4w/Z+8YN4d8RoZrSbLWd4owk6D+TDuK8KF0K/pLFYHA51geWVp0pq6a/Brs1/wH2P8ALvJsz4h4D4h9tR5qGLoS5ZRls11jJbSjJferSi9mf1uafqFlqtlFqWmyrPBOoeORDlWU8gg069vrPTbSS/v5FhghUu7ucKqjqSa/CH9j79sm++EuoQ/D/wAeSNceHbmRVjlZstZk9x6p6jt2q3+15+2fffFS8n8AfD2V7bw9CxWWZThrwj+Se3evxB+G2Zf2n9TX8Lf2nTl/+S/u/PbU/v2P0nuGv9Vf7cf+9/D9Xv73tLd/+ffXn7afF7pqftbfth3nxUu5vAXgGR7fw/A5WWUHDXZX19E9B361+Z/xKm3eCL9R3UfzFbQul6Cn+I/A3ivxR8LPEXivSbVn07RoVkurg8Iu5gAue7HPSv1HOsrwmVcN4uhRSjBUp6vq3Fq7fVt/5I/gTNeI884x4kjmeYOVWtKSdop2hCPvWjFbQjFNv5ybbuz4Toqa0ge9uoLOIhWnkSNSxwAXIUEnsBnmv0+/aK/4Jg+O/gj8Hoviz4b1n/hJFt40l1G2ig2NDG4yZEIJ3KvfgHHNfxVTw9SpGUoK6W5+xZVw1mWZYfEYrA0XOFBKU2raJ31te72b0T0R+XRIAyegr+gr/glx+yZoHhjwBc/tKfFywiafUY2OmpeIGS3sVGWmIbgF+TkjhR71+YP7DX7Lt9+1H8ZLfR75WTw5pBS61ScDKsoIKwg+snf0Ffqd/wAFSv2o4Phf4Ltv2WvhmVtrjUbRBfvA2Ps1kOFhAHQyAc9ML9a9HL6UacHi6q0W3mz9Q8M8owuV4KvxpnEL0aN40Yv/AJeVXpp5LZPo7v7J+M/7U/jX4e/EL4/+JfFXwrsI9P0Ke5K26RKESTZw0oUcAOeQBX7J/wDBFU5+HPjYf9RWH/0SK/nqACgKOgr+hT/giouPh143b11SH/0SKWVzc8YpPrf8jHwexk8XxzSxVRJSn7WTSVknKMnoui7H7a0UUV9cf3Mf/9L+/iiiigAoorzX4wfGD4afAP4bav8AF74v6xbaD4d0K3e6vb26cJHHGgyevUnoAOSeBTjFyajFXYHpVFf55Xxt/wCDu34nj9vzS/G3wX0Qz/ArQ2ksLnSp1CXurQyMA15uPMTqBmJD2+914/uU/Y//AGxfgH+3P8ENL+P37OutxazoWpoNwHyzW02PmhmjPKSKeCD9RxXqY/JcXg4QqV4WUvw8n2ZnCrGTaTPqGiiivKNDy/4u/CLwd8afBtx4N8ZW4kilBMUoH7yGTs6HsR+tfzjftA/AXxl+z54yfw34jQzWkuXs7xF/dzR/0YdxX9OPiDxBofhPQ7vxN4mu4rDT7CF57m4ncJHFFGMszMcAAAZJNf53n/Bav/g5W1H4ufGjTvg5+xB5F14E8JX4l1HVriIE6xNE2GjhLDKQdRuGC55HHX9L8Os+x2ExP1eKcsO/iX8vmvPy6/ifg3jZ4NYDjDBPFUEqeYU17k/50vsT8n0lvF+V0fq0LhTUgnA4r4y/ZG/bJ+FX7YXw9HjDwBP5N/ahV1LTZeJrSUjoR3U/wsOK+sRdL/n/APXX9G0nCrBTpu6Z/mVmuSYvLcXUwOPpOnWg7SjJWaf9ap7NarQ+pf2dP2evGH7Q3i4aLogNvp1uQ15esMpEnoPVj2Ffrd+1V8GvDnw5/YU8X+APh/Z7IrewEjYGXlZGUs7nqSQM18C/sO/ti6b8F7o/Dnx6qpoN9LvS6RRvglbjL45ZT69vpX7wX1poHjjwxNYzbL3TdUt2jbaQySRSrg4PoQa/nnxXxGaTxLwmIjy4e3uW2lpu33Xbp87v+7Po58I8L4nhfFVMuqKeY1oTp1nJe9S5k0oxWtoPfmXxve1uVfwqKA0YHYiv6Ev+CZ37bVv490eP9mb4zXAn1GKJo9Murg5F3bgYMLk9XUcD+8tflR+1/wDsn+Nv2XfiNdadqFs8vh28md9Mv1GY3iJyEY9nXoQa+UrC/v8ASr+DVdJnktbq2dZYZomKvG6nIZSOhFfztQrVMJW1Xqu5+Z8PZ5mvBWeSc4NSg+WrTeinHqv1jL56ptP+s7xHZ/A//gnR8EfE/jTwra+RHqF5JdxWpbLTXcwwkSnrsGPwXNfyrfEDx54l+J/jXU/iB4wna51LVZ3nmdj3Y8KPQKOAPQV2vxX/AGhvjT8corC3+K2vz6vFpq7beNgERT3YqvBY92NeNVeOxirNRpq0Fsju8RePKWfTo4TLqPscFRXuU9F7z+KTSuvJK7srvqwr+ir/AIIuaVd2/wAH/FesSIRDd6uFjb+8Y41Dfka/BX4YfCzx78ZfGVr4C+G+nyajqV22Aqj5I17u7dFUdya/r+/ZV+Aenfs2fBLSPhbZyC4ntVaW7nAx5tzKd0jfTJwPYV1ZLQk63tbaI+w8AOHcXiM8ebcjVClGS5ujlJWUV3sm27baX3R9FUUUV9Uf2gf/0/7+KKKKACv4If8Ag8QT9vN9W8IsVk/4Z+WJedOL7f7Xyd32/HGNu3yc/LnPev73q84+Lnwj+G/x3+HGr/CT4uaRba74d123e1vbK6QPHJG4weD0I6gjkHkV6WUY9YLFQxDgpJdP8vMipDmi0f4W1frt/wAEhP8Agrt8af8AglD8b38V+Fo21zwPr7xp4i0B3KpcRoeJoTyEnjBO04+boeK+m/8AguZ/wQz+I3/BMD4kyfEn4Ww3fiD4Oa5KzWWolC76XKx4tbphwOuI3PDAc81/PdX7LCeFzHC3VpU5f18mjympU5eZ/t9fsk/tb/Av9tv4G6N+0F+z3rUWs6BrEQYFCPNt5cfPDMnVJEPDKf5V794h8Q6F4T0O78TeJ7uGw06wiae4uZ3EcUUaDLMzHAAA6k1/j9f8EiP+Cunxv/4JTfHAeKPCZfWfAuuyRx+IvD8jkRTxg486Lsk8YJ2n+Loa/V7/AILy/wDBxZd/t2eHl/Zc/Y6mu9I+Gl1DDNrWoSBoLvUpGAY2+OqQoeH/AL5GOlfneI4OxCxio0taT+12Xn59u53xxMeW73ND/g4M/wCDgzVP2yNV1H9jz9j3UZrD4ZWE7waxrEDlH110ONiEYItgQe/7z6V/I6AAMDgCgAKNo6Cv0j/4Jkf8Ex/j/wD8FOvj/Y/Cj4UWE9voFvNGdf18xk2um2pPzEt0MhGdiZyTX6FhsNhctwvLH3YR1bfXzfn/AEjhlKVSR77/AMEMf2Rf2v8A9qr9tPRrb9mNpdL0fSp438UaxKjNYW+nk/PHKOA7uoIjTrnniv7Lfj98CvG37PPjiXwj4uiLxNl7S7UYjuIuzD39R1Ffvt+wn+wd+z5/wTy+A+n/AAF/Z70pbKyt1V728cA3V/c4w0079WYnoOijgV7V8cPgb4G+Pngqfwb41twwYEwXCgebBJ2ZT/MdDXi5N4mTwmYWqRvhXpb7S/vL9V28z8c8YfBXC8XYL61hbQx9Ne7LpNfyT8v5ZfZfkfyXi5r9Lf2Jv24bn4S3UHwz+JkzT+HZ5AsNy5LNZlu3vHn8q+KPj38CPHf7PPjabwn4yt2ELMxtLsD91cRg8Mp6Z9R2rxAXAPANfuePyzL89y/2c7TpTV1JdOzT6Nf8Bn8C5FnGfcEZ79Yw96OJpPlnCS0a6xkusX/k4u9mf2IeK/B/w++Mngt9C8U2ltrWi6lEGCuA6OrDhlPY+hHNfztftw/8E4tN+AGlTfE34ba3HJo0koVdMvGC3CFv4Ym/5aAenBArvf2PP2+9R+CGmv4B+JSy6joEUbtaOp3TQOBkRj1Rjx7V8uftEftH+Nf2i/G7+KPEzmG0hyllZqT5cEef1Y9zX4LT8GMTisynhsY7UI6qot5J7Jefe+i87o/prxI8YuEM/wCF6WM+rc2ZSXKo6qVJrdykvih/Ktebsmnb4DkilicxyqVYdQRzXUaN4R1HVMSzjyIf7zDk/QV6dIlpJIJ5Y1Z16MRk1+qf7DX7Ed58ULmH4p/Fe2kt/D8Dq9paSDabwjncf+mf/oX0rKXg3lOR+0zDPMW6lCL92EVyufZN3vfyjbvdI/AeFsJnHFOPp5TktD97L4pP4YLrJu2iXnq3ok20es/8Erv2f/G/gf8AtD4ozj7Bo2pwiFIpY/3t2VOQ4J5VFzx659q/aKq9paWthax2VlGsUMShERBtVVHAAA6AVYr4LNcdTxWIdSjRjSpqyjGKslFber7t6tn+k3APB1LhjJaOUUqsqjjdylJ/FKTvJpfZV9orbzd2yiiivNPsj//U/v4ooooAKKKKAPO/iz8Jvh18c/h1q/wm+LGk2+ueHtdt3tb2yukDxyxuMEEHoR1B6g81/lm/8Fy/+CFfxG/4Jh/ENvid8J4bzxF8Htdmke1vliaRtHctxbXTAEBecRyHAbGDzX+q54j8R6B4Q0C88U+KbyHT9N0+F7i5ubhxHFFFGMszMcAADqa/zM/+Dhb/AIL06p+3f4rvP2Tf2Xr6S0+Eui3DR397GcHXriM8N7W6EfIP4jz6V9fwfPGLFctD+H9q+3/D9jmxKjy+9ufyq0UAY4or9ZPMP0v/AOCX3/BLf9oT/gqP8d4Phf8ACa0lsvDtjLG3iDxDJGTa6bbse56NKwB8uPOSfav9ZX9hD9hT4Df8E8v2fdK/Z7+AenLbWNkoe8vHUfab+6I+eeZhyWY9B0UcCv8AKC/4JUf8FV/j1/wSu+PCfEf4aSHUvC+rPHH4i0CViIL63U43D+7MgJKN+B4r/Wd/Yy/bM+BH7eHwH0j9oL9n7Vo9S0fU4182LI8+0nx88MydVdTxz16ivzbjZ43nipfwOlu/n59uh6GE5Labn1ZRRRXwB2Hi3x3+BPgj9oHwJceCPGcIIYFre4UfvYJezKf5jvX8vH7QvwB8d/s4eOZfB/jKEtDIS9neKP3VxFngqfX1Hav6gvj58e/An7PHgK48ceN7gLtBW2twf3txL2RR/M9hX8rX7Qn7Rnjz9o3x5L418ZyhUXKWlqh/dW8WeFUevqe5r988G4Zu3Ut/ueu/839z/wBu6fM/jj6UdPhlwo8y/wCFTS3Lb+H/ANPf/bPtf9unlQuAec077SPWueFznrTxc1+/eyP4udE/XX9g79h24+K8tv8AF74qQvD4fgkDWdo64N4V53H/AKZg/wDfX0r+ge0tLWwtY7KyjWKGJQiIgwqqOAAOwFfzc/sIft2XnwO1KH4ZfEeVp/Ct5L8k7Es9k7YHH/TMnkjt1r+kDTNT07WtOg1fSJ0ubW5QSRSxncjowyCCOoNfyr4q0s3jmreYfwtfZW+Hl/8Akv5r6/Kx/or9HSXDX+rqhkqtidPb81vac/d/3P5Lab/auXqKKK/Lz+gwooooA//V/v4ooooAKxfEniTQPB2gXnirxVew6dpunQvcXV1cOI4oYoxlndjgAADJJrar/PV/4Ozf+CiX7Xlr8Yrf9hCx0u98GfDaS0iv5L1GZT4iZs5HmKceTERgx9d3LcYr08py2eOxMaEXbu/L9SKk1CN2fIX/AAcD/wDBfrXv27vFF1+yx+ylqFzpnwl0id476+icxSa/MhwGOMEWykHYv8fU9hX8qoAAwOAKUAAYFfqj/wAEnf8AglH8cv8Agqp8ek+Hvw/R9M8I6NJFJ4k19lzHZW7k/ImeGmcAhF/E8V+xUKGFyzC2Xuwju/1fds8tuVSXmM/4JQ/8Epfjr/wVU+Pcfw5+HiPpXhPSXjl8ReIZEJhsoGP3E7PO4B2J+J4r7o/4Li/8EC/H3/BL/UYPjH8Hp7vxV8JNQMcL3sy7rnTLkgDbcFRjZI3KPwATg9q/0rP2MP2MPgL+wZ8BdI/Z5/Z60hNM0bS4x5kpANxeTn7887gAvI55JPToOK9y+J/ww8AfGfwBqvwu+KOlW+t6Brdu9re2V0gkilicYIIP6HqDXwVbjSu8YqlNfulpy9139e3Y7VhY8tnuf4VdfqD/AMErP+Cpvx1/4Jb/ALQNn8S/h7cS6j4VvpUj8QeH2kIt723zgsB0WVRyjetffn/BeH/ghJ4x/wCCZvjlvjP8EYbvXPg5rk7GKcqZJdGmc5FvOwH+rOcRyH0wea/nCr9ApVcNmOGuvehL+vk0cLUqcvM/24v2Mf20PgH+3l8CdK/aA/Z61iPVNI1FF86LI+0Wc+PnhnTqjqeOevUcV3nx/wD2gfh/+zp4CuPHHjq5CBQVtrZT+9uJeyIP5noBX+Ud/wAEL/25f2t/2NP2u7A/s7xPrPhzW5Yk8T6LOzCyls1PzTE9I5UXJRupPHIr+p39o79pXx/+0v8AEGbxv42l2RrlLO0QnyreLPCqPX1PUmvM4b8KauYZg5VJWwkdW/tP+6vPu+i8z8r8VvF3D8L4P6vhbTx017sekF/PL/21fafkjV/aF/aN8e/tHePZ/GvjOc+XuK2lopPlW8WeFUevqe9eFfasDmsL7UB1r9kv+Cen/BPuX4mPa/Gv41Wrw6HE4k0/T5FwbsjkO4PPl56D+L6V/QWbZjlnDmW+1q2hSgrRit2+kYrq/wDh2fw9kXDmdcZ526NK9SvUfNOctorrKT6JdF6JIh/Yq/4JyXXxq8MSfEn4wtPpukXkLLp1vH8s0hYcTHPRR1Ud6+KP2nP2bvHX7MXj+Twl4pUz2U+Xsb5QRHcRZ/Rh/Etf2D2trbWNtHZ2caxRRKEREGFVRwAAOgFeSfHL4G+Af2gvAVz4A8f2wmt5huimUDzYJB0dD2I/Wv5/yrxgx0c3niMcr4abtyL7C6OPdrr/ADeWlv604g+jdlFTh6ngsrfLjaauqj/5eS6xn2i/s2+Hz1v/ABi+d3r9O/2DP28r/wCBGpRfDT4lSvdeFL2UBJmYs9izcZX1j7kduor48/ah/Zr8bfsu/EWTwZ4pHn2c4MtheqMJcQ5IB9mHRhXzd9oAFf0Djsuy3iHLeSdqlGorpr8Gn0a/4DW6P5DyrMc74Mzz2tG9LE0XaUXs11jJdYv/ACaezP7pdK1bTNd02DWdGnS6tLlBJFLEwZHRuQQR1FaFfix/wSG1n47X3hPVLHXUL+BoT/oEtxneLjPzLD6pjr2B6d6/aev424nyP+yMyrZf7RT5Huvv17NdV0Z/pTwPxP8A6w5Lh82dGVJ1FrGXdaNp9YveL6oKKKK8A+sP/9b+/iiiigAr4E/4KI/8E4f2b/8AgpZ8DLr4M/H7SklljV5NJ1aJQLzTblhxLC/Uc43L0YcGvvuitKNadKaqU3aS2Ymk1Zn+Vt8Nf+DZH9vDxJ/wUEn/AGQfGti+m+DdMkF5eeNlTNjLpRb5Xgz964cfL5XVWyTx1/0lv2L/ANif9nv9gn4H6b8Bv2dNDh0jSrFF8+YKDcXs4GGmuJOskjHPJ6dBxX1lgZz3pa9bNc+xWPjGFV2iui6vu/60M6dKMNgooorxTU4T4m/DHwB8ZfAeqfDH4paRba7oGtQPbXtjeRiWGaJxghlII/wr/M//AOCw/wDwbq/En9kb9o7Ttc/ZhQ6h8KvGl4VgknkUyaJIxy0UmTueMDmNgCexr/SN/aA/aA+Hf7N3w6u/iL8RbtYYIFIggBHm3Ev8Mca9yfyA5NfyB/tTftZfEX9qv4gSeL/GEv2exgLJYWEZPlW8WeOO7H+Ju9fsXhRwnmOZYl4hNwwi+Jv7T/lj5930Xnofj3iv4nYThrCPD0bTxs17kekV/PPy7L7T8rn58fs1fs1/Df8AZg8Dp4U8CwB7qYK19fuAZrmQDkseyjsvQV9GfaWrAWcjvUnnt6mv62w+Cp0KapUo2itkfwFmOLxWPxNTGYyo51Zu8pN6t/1stktEftx/wTa/YHsfi6sHx2+L8aT6BFJnT7DcGFy6dWlAzhQf4T171/SBaWltY20dlZRrFDEoREQYVVHAAA6AV/Hv+xJ+3N4y/ZO8Wi0ui+oeE9QkX7dYk5KdjLFzw49Ohr+tj4c/Efwb8WPB1l498A30eoaZqEYkiljOevVWHZh0IPIr+TPGXLs6p5p9Zxz5sO9KbXwxX8rXSXd/a3Wmi/t76P8AmHD08l+qZZDkxUdaydueT/mT0vDsl8Oz1d33FFFFfjR/QB4x8dPgN8O/2hvA1x4F+Idms8MgJhmAxLbydnjbqCP1r8RPg3/wSV8Z/wDC9r7T/izMreDNIlEkM8TYfUVPKpgcoAPv+/Ar+iKivrsh43zbKMLWweCq2hUXXXlf80eza0/HdJnwPFHhpkHEGOw+YZlQ5qlJ7rTnXSM/5op6/hs2jD8NeGdA8HaHbeGvC9nFYWFmgjhghUIiKOwArcoor5Oc5Tk5Sd292fd06cacVCCtFaJLZLsgoooqSz//1/7+KKKKACiiigAooooAK8J/aK/aG+H37M/wzvPiX8QrgRwwDbb26kebczH7saDuSep7DmvdW3bTt69s1/Hj/wAFS9c/acu/2hbiw+Psf2fTYWf+w47bd9ha2zw0ZPWQj7+eQfav0Dw44PpcRZssLXqqFOK5pK9pSS6RXfu+i1PzvxN4zrcN5PLF4ei51JPli7XjFv7U327Lq9Dwr9qv9rn4lftZ+Pv+Ev8AG8i29na7ksNPiJ8m2iJ7Ak5Y/wATHrXy/wDacDJNYfn45PFftR/wTX/4Ju6j8aryz+OXxttpLXwtbSrJY2Mi7W1Bl53MD0hB/wC+vpX9jZpmGU8LZT7WolTo01aMVu30jFdW/wDNvqz+HcryTOeLs4dODdSvUd5Tlsl1lJ9Eui9Elsix/wAE8/8Agmpc/Hq3HxZ+OcFxY+F8f6Daj93Jen++eMiMdum76V88ft4fsM+LP2RvGH9p6MJtS8G6gxNnfMMmFj/yxmIAAYfwnuPev7DbGxs9Ms4tP0+JYIIFCRxoNqqq8AADoBXL+P8AwB4R+KHhG+8C+OrGPUNM1CMxTQyjIIPcehHUEdDX8x4PxqzWOdvH11fDS0dJbKPRp/zrdvrtta39V47wCyWeQRy7D6YqOqrPeUuqkv5Hsl9ndXd7/wACwuGHevvT9iL9u7x1+yP4n+wMDqXhPUJVN/YMTlOxlh/uuB+BqH9vD9hXxl+yD4v/ALS03zNT8HajIfsV8VyYSf8AljNjgMOx/iHvX59C6bHav6fjDKeJsqurVcPVX9ecZRfzTP5LdLOeE850vRxNJ/15SjJfJo/v3+GnxJ8HfF3wRp/xC8BXiX2l6lEJYZEPr1Vh2YdCDyDXd1/PD/wRa8KftJW8moeKfPNp8N7kMBBdKT9ouR/Hbgn5QP4m6Gv6Hq/iHjXh6lkmb1svoVlUjF6Nbq/2ZdOZdbfhsf6AcC8SVs9yahmWIoOlOS1T2dvtR68r3V/x3ZRRRXyh9eFFFFABRRRQB//Q/v4ooooAKKKKACiiigAr5u/aj/Zg+HX7VvwyuPh14+i2N/rLO8jA861mHR0Pp2YdCOK+kaK6sDjq+DxEMVhZuFSDumt00cmOwOHxuHnhcVBTpzVpJ7NM/nF/ZW/4I2eINL+MV9rH7Rk0Vz4d0G5H2GCA8anjlXfuiDjcvJJ46V/RfY2FlpdlFpumxJBbwII444wFVEUYAAHAAFW6K9/injHM+Ia8a+Y1L8qsorSK7tLu3q3+iSPn+E+C8q4dw86GW07czvJvWT7Jvstkv1bYUUUV8sfVnEfEb4c+Dvix4Mv/AAB49sY9Q0vUYjFNDIMjB7j0YdQRyDX4HeH/APgiNJB+0LKNe1vzvhzARcxBeLyUEn/R27ADu46jtmv6KKK+r4d42zjI6Vajl1ZxjUVmt7P+aN9pW0uv0R8lxJwNk2e1aFfMqCnKk7p7XX8srbxvrZ/qzn/CnhXw/wCCPDll4R8K2sdlp2nQrBbwRDCoiDAAFdBRRXy05ynJzm7t6tvqfVwhGEVCCsloktkgoooqSgooooAKKKKAP//R/v4ooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKAP/Z",
              "contactLink": "simplex:/contact#/?v=2&smp=smp%3A%2F%2Fu2dS9sG8nMNURyZwqASV4yROM28Er0luVTx5X1CsMrU%3D%40smp4.simplex.im%2FShQuD-rPokbDvkyotKx5NwM8P3oUXHxA%23%2F%3Fv%3D1-2%26dh%3DMCowBQYDK2VuAyEA6fSx1k9zrOmF0BJpCaTarZvnZpMTAVQhd3RkDQ35KT0%253D%26srv%3Do5vmywmrnaxalvz6wi3zicyftgio6psuvyniis6gco6bp6ekl4cqj4id.onion",
              "localAlias": ""
            },
            "contactUsed": true,
            "contactStatus": "active",
            "chatSettings": {
              "enableNtfs": "all",
              "favorite": false
            },
            "userPreferences": {},
            "mergedPreferences": {
              "timedMessages": {
                "enabled": {
                  "forUser": true,
                  "forContact": true
                },
                "userPreference": {
                  "type": "user",
                  "preference": {
                    "allow": "yes"
                  }
                },
                "contactPreference": {
                  "allow": "yes"
                }
              },
              "fullDelete": {
                "enabled": {
                  "forUser": false,
                  "forContact": false
                },
                "userPreference": {
                  "type": "user",
                  "preference": {
                    "allow": "no"
                  }
                },
                "contactPreference": {
                  "allow": "no"
                }
              },
              "reactions": {
                "enabled": {
                  "forUser": true,
                  "forContact": true
                },
                "userPreference": {
                  "type": "user",
                  "preference": {
                    "allow": "yes"
                  }
                },
                "contactPreference": {
                  "allow": "yes"
                }
              },
              "voice": {
                "enabled": {
                  "forUser": true,
                  "forContact": true
                },
                "userPreference": {
                  "type": "user",
                  "preference": {
                    "allow": "yes"
                  }
                },
                "contactPreference": {
                  "allow": "yes"
                }
              },
              "calls": {
                "enabled": {
                  "forUser": true,
                  "forContact": true
                },
                "userPreference": {
                  "type": "user",
                  "preference": {
                    "allow": "yes"
                  }
                },
                "contactPreference": {
                  "allow": "yes"
                }
              }
            },
            "createdAt": "2025-05-03T08:13:55.287368Z",
            "updatedAt": "2025-05-03T08:13:55.287368Z",
            "chatTs": "2025-05-03T08:13:55.287368Z",
            "contactGrpInvSent": false,
            "chatTags": [],
            "chatDeleted": false
          }
        },
        "chatItems": [],
        "chatStats": {
          "unreadCount": 0,
          "unreadMentions": 0,
          "reportsCount": 0,
          "minUnreadItemId": 0,
          "unreadChat": false
        }
      },
      {
        "chatInfo": {
          "type": "local",
          "noteFolder": {
            "noteFolderId": 1,
            "userId": 1,
            "createdAt": "2025-05-03T08:13:55Z",
            "updatedAt": "2025-05-03T08:13:55Z",
            "chatTs": "2025-05-03T08:13:55Z",
            "favorite": false,
            "unread": false
          }
        },
        "chatItems": [],
        "chatStats": {
          "unreadCount": 0,
          "unreadMentions": 0,
          "reportsCount": 0,
          "minUnreadItemId": 0,
          "unreadChat": false
        }
      }
    ]
  }
}
```

**Response Type:** `chats`


## Summary

This document covers the most commonly used SimpleX WebSocket API commands. For complete details, refer to the official SimpleX documentation or the source code of the SimpleX Chat application.

### Notes on Response Types

- `cmdOk`: Indicates the command was executed successfully with no specific return data
- `activeUser`: Contains information about the currently active user
- `usersList`: Contains a list of all users
- `userContactLink`: Contains the contact link for a user
- `chats`: Contains a list of all chats
- `chat`: Contains information about a specific chat
- `chatCmdError`: Indicates an error occurred when executing the command
- `groupCreated`: Contains information about a newly created group
- `userServers`: Contains information about the user's servers
