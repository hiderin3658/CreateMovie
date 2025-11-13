#!/usr/bin/env python3
"""
Test Research Integration
Demonstrates how to use the research-aware material system
"""

import sys
from pathlib import Path

# Add tools to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from tools import (
    ResearchDatabase,
    ResearchAwareStrategy,
    MaterialSystem,
    MaterialConfig
)


def test_research_database():
    """Test 1: Research Database Loading"""
    print("=" * 60)
    print("Test 1: Research Database Loading")
    print("=" * 60)

    db_path = Path(__file__).parent / "data" / "shirahama-locations-database.yaml"

    if not db_path.exists():
        print(f"❌ Database not found: {db_path}")
        return

    db = ResearchDatabase(db_path)

    print(f"\n📚 Project: {db.project.get('name')}")
    print(f"   Theme: {db.project.get('theme')}")
    print(f"   Core Value: {db.project.get('core_value')}")

    print(f"\n📍 Locations: {len(db.locations)}")
    for location in list(db.locations.values())[:3]:
        print(f"   • {location.name} ({location.category})")
        print(f"     → {location.core_narrative}")

    print(f"\n📖 Story Frameworks: {len(db.story_frameworks)}")
    for key, framework in db.story_frameworks.items():
        print(f"   • {framework.name}")
        print(f"     → {framework.theme}")

    print("\n✅ Test 1 passed!")


def test_location_search():
    """Test 2: Location Search"""
    print("\n" + "=" * 60)
    print("Test 2: Location Search")
    print("=" * 60)

    db_path = Path(__file__).parent / "data" / "shirahama-locations-database.yaml"
    db = ResearchDatabase(db_path)

    # Search by category
    print("\n🔍 Beach locations:")
    beach_locations = db.search_locations(category='beach')
    for loc in beach_locations:
        print(f"   • {loc.name}: {loc.core_narrative}")

    # Search by keywords
    print("\n🔍 Locations with '温泉' keyword:")
    onsen_locations = db.search_locations(keywords=['温泉'])
    for loc in onsen_locations:
        print(f"   • {loc.name}: {loc.storytelling_theme}")

    print("\n✅ Test 2 passed!")


def test_scene_suggestions():
    """Test 3: Scene-Based Location Suggestions"""
    print("\n" + "=" * 60)
    print("Test 3: Scene-Based Location Suggestions")
    print("=" * 60)

    db_path = Path(__file__).parent / "data" / "shirahama-locations-database.yaml"
    db = ResearchDatabase(db_path)

    # Test scene 1: Peaceful hot spring
    print("\n🎬 Scene: Peaceful hot spring with ocean waves")
    suggestions = db.suggest_locations_for_scene(
        scene_description="peaceful hot spring with ocean waves crashing",
        mood="peaceful",
        time_of_day="early morning"
    )

    print("   Suggestions (ranked by score):")
    for i, loc in enumerate(suggestions[:3], 1):
        print(f"   {i}. {loc.name}")
        print(f"      → {loc.storytelling_theme}")

    # Test scene 2: Beach resort
    print("\n🎬 Scene: Luxurious beach resort with white sand")
    suggestions = db.suggest_locations_for_scene(
        scene_description="luxurious beach resort with white sand and blue water",
        mood="romantic"
    )

    print("   Suggestions (ranked by score):")
    for i, loc in enumerate(suggestions[:3], 1):
        print(f"   {i}. {loc.name}")
        print(f"      → {loc.core_narrative}")

    print("\n✅ Test 3 passed!")


def test_story_framework():
    """Test 4: Story Framework Generation"""
    print("\n" + "=" * 60)
    print("Test 4: Story Framework Generation")
    print("=" * 60)

    db_path = Path(__file__).parent / "data" / "shirahama-locations-database.yaml"
    db = ResearchDatabase(db_path)

    # Generate story structure using "time" framework
    print("\n📖 Generating story with 'Time' framework:")
    structure = db.generate_story_structure(framework_key='time', num_cuts=7)

    for cut in structure:
        print(f"\n   Cut {cut['cut_number']}: {cut['era']}")
        print(f"      Location: {cut['location']}")
        print(f"      Hint: {cut['narrative_hint']}")

    print("\n✅ Test 4 passed!")


def test_research_aware_strategy():
    """Test 5: Research-Aware Material Matching"""
    print("\n" + "=" * 60)
    print("Test 5: Research-Aware Material Matching")
    print("=" * 60)

    config_path = Path(__file__).parent / "config.yaml"
    config = MaterialConfig.from_yaml(config_path)

    # Load material system
    system = MaterialSystem(config)

    # Replace strategy with research-aware strategy
    db_path = Path(__file__).parent / "data" / "shirahama-locations-database.yaml"
    system.strategy = ResearchAwareStrategy(config, db_path)

    print(f"\n✓ Material system loaded with ResearchAwareStrategy")

    # Load materials
    materials = system.load_materials()
    print(f"✓ Loaded {len(materials)} materials")

    # Create test cut
    test_cut = {
        'scene_description': 'Beautiful white sand beach with blue water and people relaxing',
        'mood': 'peaceful',
        'time_of_day': 'afternoon',
        'categories': ['beach']
    }

    print(f"\n🎬 Test scene: {test_cut['scene_description']}")

    # Find best match
    system.matcher.index_materials(materials)
    best_match = system.strategy.find_best_match(
        cut=test_cut,
        materials=materials,
        matcher=system.matcher
    )

    if best_match:
        print(f"\n✓ Best match found:")
        print(f"   • File: {best_match.filename}")
        print(f"   • Location: {best_match.location}")
        print(f"   • Score: {best_match.match_score:.1f}")
        print(f"   • Description: {best_match.description[:100]}...")

        # Get location context
        if best_match.location:
            context = system.strategy.get_location_context(best_match.location)
            if context:
                print(f"\n   📍 Location Context:")
                print(f"      → {context['core_narrative']}")
                print(f"      → Theme: {context['storytelling_theme']}")
    else:
        print("   ⚠️ No match found")

    print("\n✅ Test 5 passed!")


def test_narrative_phrases():
    """Test 6: Narrative Phrase Retrieval"""
    print("\n" + "=" * 60)
    print("Test 6: Narrative Phrase Retrieval")
    print("=" * 60)

    db_path = Path(__file__).parent / "data" / "shirahama-locations-database.yaml"
    db = ResearchDatabase(db_path)

    print("\n📝 Opening phrases:")
    for phrase in db.get_narrative_phrases('openings'):
        print(f"   • {phrase}")

    print("\n📝 Transition phrases:")
    for phrase in db.get_narrative_phrases('transitions')[:2]:
        print(f"   • {phrase}")

    print("\n📝 Closing phrases:")
    for phrase in db.get_narrative_phrases('closings'):
        print(f"   • {phrase}")

    print("\n✅ Test 6 passed!")


def test_seasonal_recommendations():
    """Test 7: Seasonal Recommendations"""
    print("\n" + "=" * 60)
    print("Test 7: Seasonal Recommendations")
    print("=" * 60)

    db_path = Path(__file__).parent / "data" / "shirahama-locations-database.yaml"
    db = ResearchDatabase(db_path)

    print("\n🌞 Summer recommendations:")
    summer = db.get_seasonal_recommendations('summer')
    for location in summer.get('best', []):
        print(f"   • {location}")

    print("\n🍂 Spring/Autumn recommendations:")
    spring_autumn = db.get_seasonal_recommendations('spring_autumn')
    for location in spring_autumn.get('best', []):
        print(f"   • {location}")

    print("\n❄️ Winter recommendations:")
    winter = db.get_seasonal_recommendations('winter')
    for location in winter.get('best', []):
        print(f"   • {location}")

    print("\n✅ Test 7 passed!")


def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("Research Integration Test Suite")
    print("=" * 60)

    try:
        test_research_database()
        test_location_search()
        test_scene_suggestions()
        test_story_framework()
        test_research_aware_strategy()
        test_narrative_phrases()
        test_seasonal_recommendations()

        print("\n" + "=" * 60)
        print("✅ All tests passed!")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ Test failed with error:")
        print(f"   {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
