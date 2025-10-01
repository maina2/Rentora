#!/usr/bin/env python3
"""
Test script to verify all imports work correctly
"""
import sys
import os

# Add project root to sys.path
project_root = os.path.abspath(".")
if project_root not in sys.path:
    sys.path.insert(0, project_root)

def test_imports():
    try:
        print("Testing imports...")
        
        # Test base import
        from app.db.base import Base
        print("✓ Base imported (SQLAlchemy 2.0 DeclarativeBase)")
        print(f"✓ Base type: {type(Base)}")
        
        # Test models import
        from app.db.models import (
            PaymentStatus,
            Landlord, 
            Property,
            Tenant, 
            RentPayment, 
            Notification,
        )
        print("✓ All models imported")
        
        # Check metadata
        tables = list(Base.metadata.tables.keys())
        print(f"✓ Tables detected: {tables}")
        
        if not tables:
            print("❌ No tables detected! This is the problem.")
            return False
            
        print("✓ All imports successful!")
        return True
        
    except Exception as e:
        print(f"❌ Import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)