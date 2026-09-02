# Session 9 Implementation: RAG Knowledge Base

## 📌 Quick Start

### 1. Start Backend
```bash
cd backend
python -m uvicorn main:app --reload
```

### 2. Run Tests
```bash
# From project root
python test_rag.py
```

This will:
- Register a test user
- Login to get JWT token
- Test 5 different RAG queries
- Verify security (auth required)
- Show source citations

### 3. Manual Testing
```bash
# Register
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test",
    "email": "test@example.com",
    "password": "pass123"
  }'

# Login (copy access_token)
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "pass123"
  }'

# Ask question
curl -X POST "http://localhost:8000/api/v1/ask" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Do I need a visa to visit Japan?"
  }'
```

## 📁 Files Added/Modified

### New Files
- ✅ `backend/services/kb_service.py` - Knowledge Base integration
- ✅ `travel-guides/visa-japan.md` - Visa info
- ✅ `travel-guides/tokyo-attractions.md` - Tokyo guide
- ✅ `travel-guides/packing-checklist.md` - Packing tips
- ✅ `travel-guides/travel-insurance.md` - Insurance info
- ✅ `test_rag.py` - Automated test suite
- ✅ `SESSION_9_SUBMISSION.md` - Full documentation

### Modified Files
- ✅ `backend/schemas.py` - Added QuestionRequest, AssistantResponse
- ✅ `backend/main.py` - Added /api/v1/ask and /api/v1/assistant endpoints

## 🎯 What was Implemented

### Core Features
1. **RAG Pipeline**: Retrieve documents → Generate answers
2. **Knowledge Base Service**: `backend/services/kb_service.py`
   - Handles Bedrock API calls
   - Mock responses for testing (no AWS needed)
   - Source citation tracking

3. **Two API Endpoints**:
   - `POST /api/v1/ask` - Main endpoint
   - `POST /api/v1/assistant` - Semantic alias

4. **Response Format**:
   ```json
   {
     "question": "...",
     "answer": "...",
     "sources": [
       {"document": "visa-japan.pdf", "source": "..."}
     ]
   }
   ```

### Security
- ✅ JWT authentication required
- ✅ AWS credentials on backend only
- ✅ Frontend never calls Bedrock directly

### Documents Prepared
All ready for S3 upload to AWS:
- `visa-japan.md` - Complete visa requirements
- `tokyo-attractions.md` - 2-3 day itinerary with costs
- `packing-checklist.md` - Seasonal packing lists
- `travel-insurance.md` - Coverage types and costs

## 🚀 Testing

### Automated Testing
```bash
python test_rag.py
```

Tests:
1. User registration
2. User login
3. Visa question → visa-japan.md
4. Attractions question → tokyo-attractions.md
5. Packing question → packing-checklist.md
6. Insurance question → travel-insurance.md
7. Baggage question → travel guide
8. /api/v1/assistant endpoint
9. Security: No auth header
10. Security: Invalid token

**Expected Output**: ✅ All 10 tests passed

## 🔧 AWS Setup (Optional - for production)

```bash
# Create S3 bucket
aws s3 mb s3://kelana-travel-docs

# Upload documents
aws s3 sync travel-guides/ s3://kelana-travel-docs/

# Create Knowledge Base in AWS Console
# Then set environment variable:
export BEDROCK_KB_ID="your-kb-id"

# Restart backend - it will use real Bedrock API
```

## 📊 Architecture

```
Frontend (Next.js)
    ↓ (JWT token)
Backend FastAPI
    ↓ (Question)
AWS Bedrock Knowledge Base
    ↓ (Retrieve + Generate)
Response with Sources
    ↓
Frontend displays answer + citations
```

## ✅ Completion Checklist

- ✅ Service layer created (kb_service.py)
- ✅ Endpoints implemented
- ✅ Schemas updated
- ✅ 4 travel documents prepared
- ✅ Mock mode working
- ✅ JWT authentication
- ✅ Test suite created (10 tests)
- ✅ Documentation complete
- ✅ Ready for Git commit

## 📝 Submission Files

For teacher review:
- `SESSION_9_SUBMISSION.md` - Detailed documentation
- `test_rag.py` - Automated verification
- All implementation files (source code + docs)

## 🎓 Learning Outcomes

✅ Understand RAG architecture and benefits  
✅ Implement retrieval-augmented generation  
✅ Secure backend-owned API calls  
✅ Provide source citations in responses  
✅ Test ML/AI features thoroughly  

## 🔗 Related Files

- Backend Main: `backend/main.py`
- DB Layer: `backend/database.py`
- Auth: `backend/services/auth_service.py`
- Trips: `backend/services/trip_service.py`
- All tests: `test_rag.py`

---

**Status**: ✅ Complete and ready for submission  
**Last Updated**: 2025-09-02
