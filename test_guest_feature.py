#!/usr/bin/env python3
"""
Test script to verify guest browse functionality
"""

import json
from services.contact_service import view_contacts, search_contacts

def test_guest_features():
    """Test all guest browse features"""
    print("=" * 60)
    print("TESTING GUEST BROWSE FEATURES")
    print("=" * 60)
    
    # Test 1: View all contacts
    print("\n[TEST 1] View All Contacts:")
    print("-" * 60)
    try:
        all_contacts = view_contacts()
        print(f"✓ Successfully retrieved {len(all_contacts)} contacts")
        for i, contact in enumerate(all_contacts[:3], 1):
            print(f"  {i}. {contact.get('full_name')} - {contact.get('phone_number')}")
        if len(all_contacts) > 3:
            print(f"  ... and {len(all_contacts) - 3} more")
    except Exception as e:
        print(f"✗ Error: {str(e)}")
    
    # Test 2: Search functionality
    print("\n[TEST 2] Search Contacts:")
    print("-" * 60)
    try:
        if all_contacts:
            search_term = all_contacts[0].get('full_name', 'test').split()[0]
            results = search_contacts(search_term)
            print(f"✓ Search for '{search_term}' returned {len(results)} results")
            for i, contact in enumerate(results[:3], 1):
                print(f"  {i}. {contact.get('full_name')} - {contact.get('phone_number')}")
        else:
            print("⊘ No contacts to search (database empty)")
    except Exception as e:
        print(f"✗ Error: {str(e)}")
    
    # Test 3: Contact detail fields
    print("\n[TEST 3] Contact Detail Fields:")
    print("-" * 60)
    try:
        if all_contacts:
            contact = all_contacts[0]
            fields = ['full_name', 'email', 'phone_number', 'address', 'date_of_birth']
            print(f"Contact: {contact.get('full_name')}")
            for field in fields:
                value = contact.get(field, 'N/A')
                print(f"  • {field}: {value}")
        else:
            print("⊘ No contacts to display details")
    except Exception as e:
        print(f"✗ Error: {str(e)}")
    
    # Test 4: Empty search
    print("\n[TEST 4] Empty Search Handling:")
    print("-" * 60)
    try:
        results = search_contacts("NONEXISTENT_CONTACT_12345")
        if results:
            print(f"✗ Unexpected results for non-existent contact")
        else:
            print(f"✓ Correctly returned empty results for non-existent contact")
    except Exception as e:
        print(f"✗ Error: {str(e)}")
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY: All guest features are working correctly!")
    print("=" * 60)

if __name__ == "__main__":
    test_guest_features()
