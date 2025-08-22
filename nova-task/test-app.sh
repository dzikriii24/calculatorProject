#!/bin/bash

echo "🧪 Testing Nova Task Application"
echo "==============================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to test backend connection
test_backend() {
    echo "🔍 Testing backend connection..."
    if curl -s http://127.0.0.1:8080 > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Backend server is accessible${NC}"
        return 0
    else
        echo -e "${RED}❌ Backend server is not accessible${NC}"
        return 1
    fi
}

# Function to test frontend build
test_build() {
    echo "🔨 Testing frontend build..."
    if npm run build > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Frontend builds successfully${NC}"
        return 0
    else
        echo -e "${RED}❌ Frontend build failed${NC}"
        return 1
    fi
}

# Function to test dependencies
test_dependencies() {
    echo "📦 Testing dependencies..."
    if [ -d "node_modules" ]; then
        echo -e "${GREEN}✅ Dependencies are installed${NC}"
        return 0
    else
        echo -e "${RED}❌ Dependencies are not installed${NC}"
        return 1
    fi
}

# Function to test Node.js version
test_node_version() {
    echo "🟢 Testing Node.js version..."
    NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
    if [ "$NODE_VERSION" -ge 18 ]; then
        echo -e "${GREEN}✅ Node.js version: $(node -v)${NC}"
        return 0
    else
        echo -e "${RED}❌ Node.js version 18+ required. Current: $(node -v)${NC}"
        return 1
    fi
}

# Run all tests
echo "Starting tests..."
echo ""

test_node_version
NODE_OK=$?

test_dependencies
DEPS_OK=$?

test_build
BUILD_OK=$?

test_backend
BACKEND_OK=$?

echo ""
echo "📊 Test Results Summary"
echo "======================"

if [ $NODE_OK -eq 0 ]; then
    echo -e "${GREEN}✅ Node.js Version${NC}"
else
    echo -e "${RED}❌ Node.js Version${NC}"
fi

if [ $DEPS_OK -eq 0 ]; then
    echo -e "${GREEN}✅ Dependencies${NC}"
else
    echo -e "${RED}❌ Dependencies${NC}"
fi

if [ $BUILD_OK -eq 0 ]; then
    echo -e "${GREEN}✅ Frontend Build${NC}"
else
    echo -e "${RED}❌ Frontend Build${NC}"
fi

if [ $BACKEND_OK -eq 0 ]; then
    echo -e "${GREEN}✅ Backend Connection${NC}"
else
    echo -e "${YELLOW}⚠️  Backend Connection (not critical for frontend testing)${NC}"
fi

echo ""
if [ $NODE_OK -eq 0 ] && [ $DEPS_OK -eq 0 ] && [ $BUILD_OK -eq 0 ]; then
    echo -e "${GREEN}🎉 All critical tests passed! The application is ready to run.${NC}"
    echo ""
    echo "To start the application:"
    echo "  ./start-dev.sh"
    echo ""
    echo "Or manually:"
    echo "  npm run dev"
else
    echo -e "${RED}❌ Some tests failed. Please fix the issues above.${NC}"
    exit 1
fi