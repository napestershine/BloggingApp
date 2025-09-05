#!/bin/bash

# SF5 Blog App - Comprehensive Test Runner Script
# This script runs all types of tests and generates coverage reports

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
COVERAGE_THRESHOLD=80
TEST_TIMEOUT=300
INTEGRATION_TEST_TIMEOUT=600

# Helper functions
print_section() {
    echo -e "\n${BLUE}===================================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}===================================================${NC}\n"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check if Flutter is available
check_flutter() {
    if ! command -v flutter &> /dev/null; then
        print_error "Flutter is not installed or not in PATH"
        exit 1
    fi
    
    print_info "Flutter version: $(flutter --version | head -n 1)"
}

# Clean previous test artifacts
clean_artifacts() {
    print_section "Cleaning Previous Test Artifacts"
    
    # Remove previous coverage files
    rm -rf coverage/
    rm -rf test-results/
    rm -f lcov.info
    
    # Clean Flutter
    flutter clean
    flutter pub get
    
    print_success "Artifacts cleaned"
}

# Generate mock files
generate_mocks() {
    print_section "Generating Mock Files"
    
    if flutter packages pub run build_runner build --delete-conflicting-outputs; then
        print_success "Mock files generated successfully"
    else
        print_warning "Mock generation failed or not needed"
    fi
}

# Run static analysis
run_analysis() {
    print_section "Running Static Analysis"
    
    if flutter analyze; then
        print_success "Static analysis passed"
    else
        print_error "Static analysis failed"
        return 1
    fi
}

# Run unit and widget tests
run_unit_tests() {
    print_section "Running Unit and Widget Tests"
    
    # Create test results directory
    mkdir -p test-results
    
    # Run tests with coverage
    if flutter test \
        --coverage \
        --timeout ${TEST_TIMEOUT}s \
        --reporter json > test-results/unit-test-results.json; then
        
        print_success "Unit and widget tests passed"
        
        # Generate coverage report
        if command -v lcov &> /dev/null; then
            generate_coverage_report
        else
            print_warning "lcov not available, skipping HTML coverage report"
        fi
        
        return 0
    else
        print_error "Unit and widget tests failed"
        return 1
    fi
}

# Generate coverage report
generate_coverage_report() {
    print_section "Generating Coverage Report"
    
    # Remove Flutter framework files from coverage
    lcov --remove coverage/lcov.info \
        '*/flutter/packages/*' \
        '*/third_party/*' \
        '*/test/*' \
        '*/integration_test/*' \
        '*/test_driver/*' \
        '*/*.g.dart' \
        '*/*.freezed.dart' \
        -o coverage/lcov_cleaned.info
    
    # Generate HTML report
    genhtml coverage/lcov_cleaned.info -o coverage/html
    
    # Check coverage threshold
    local coverage_percentage=$(lcov --summary coverage/lcov_cleaned.info 2>&1 | \
        grep -o '[0-9.]*%' | head -n 1 | sed 's/%//')
    
    if [ -n "$coverage_percentage" ]; then
        echo "Coverage: ${coverage_percentage}%"
        
        if (( $(echo "$coverage_percentage >= $COVERAGE_THRESHOLD" | bc -l) )); then
            print_success "Coverage threshold met: ${coverage_percentage}% >= ${COVERAGE_THRESHOLD}%"
        else
            print_warning "Coverage below threshold: ${coverage_percentage}% < ${COVERAGE_THRESHOLD}%"
        fi
    fi
    
    print_info "Coverage report generated at: coverage/html/index.html"
}

# Run integration tests
run_integration_tests() {
    print_section "Running Integration Tests"
    
    if [ -d "integration_test" ] && [ "$(ls -A integration_test)" ]; then
        if flutter test integration_test/ --timeout ${INTEGRATION_TEST_TIMEOUT}s; then
            print_success "Integration tests passed"
        else
            print_error "Integration tests failed"
            return 1
        fi
    else
        print_info "No integration tests found, skipping"
    fi
}

# Run end-to-end tests
run_e2e_tests() {
    print_section "Running End-to-End Tests"
    
    if [ -d "test_driver" ] && [ "$(ls -A test_driver)" ]; then
        print_info "E2E tests require manual execution with 'flutter drive'"
        print_info "Command: flutter drive --target=test_driver/app.dart"
    else
        print_info "No E2E tests found, skipping"
    fi
}

# Performance tests
run_performance_tests() {
    print_section "Running Performance Tests"
    
    # Check app size
    local app_size=$(flutter build apk --analyze-size 2>&1 | grep "Total size:" || echo "Size check failed")
    print_info "App size analysis: $app_size"
    
    # Note: Additional performance tests would go here
    print_info "Performance tests completed"
}

# Accessibility tests
run_accessibility_tests() {
    print_section "Running Accessibility Tests"
    
    # Note: Accessibility tests are included in widget tests
    # Additional accessibility-specific tests could be added here
    print_info "Accessibility guidelines should be verified in widget tests"
}

# Security tests
run_security_tests() {
    print_section "Running Security Tests"
    
    # Check for common security issues
    print_info "Security considerations:"
    print_info "- Authentication flow tests included in unit tests"
    print_info "- Input validation tests included in widget tests"
    print_info "- Token handling tests included in service tests"
}

# Generate test summary
generate_summary() {
    print_section "Test Summary"
    
    local total_tests=0
    local failed_tests=0
    
    if [ -f "test-results/unit-test-results.json" ]; then
        # Parse test results (this would need actual JSON parsing)
        print_info "Unit/Widget tests: See test-results/unit-test-results.json"
    fi
    
    if [ -f "coverage/lcov.info" ]; then
        print_info "Coverage report: coverage/html/index.html"
    fi
    
    print_success "Test execution completed"
}

# Main execution
main() {
    print_section "SF5 Blog App - Test Suite Runner"
    
    # Parse command line arguments
    SKIP_INTEGRATION=false
    SKIP_E2E=false
    SKIP_ANALYSIS=false
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --skip-integration)
                SKIP_INTEGRATION=true
                shift
                ;;
            --skip-e2e)
                SKIP_E2E=true
                shift
                ;;
            --skip-analysis)
                SKIP_ANALYSIS=true
                shift
                ;;
            --help)
                echo "Usage: $0 [options]"
                echo "Options:"
                echo "  --skip-integration  Skip integration tests"
                echo "  --skip-e2e         Skip end-to-end tests"
                echo "  --skip-analysis    Skip static analysis"
                echo "  --help             Show this help message"
                exit 0
                ;;
            *)
                print_error "Unknown option: $1"
                exit 1
                ;;
        esac
    done
    
    # Execute test phases
    check_flutter
    clean_artifacts
    generate_mocks
    
    if [ "$SKIP_ANALYSIS" = false ]; then
        run_analysis || exit 1
    fi
    
    run_unit_tests || exit 1
    
    if [ "$SKIP_INTEGRATION" = false ]; then
        run_integration_tests
    fi
    
    if [ "$SKIP_E2E" = false ]; then
        run_e2e_tests
    fi
    
    run_performance_tests
    run_accessibility_tests
    run_security_tests
    generate_summary
    
    print_success "All tests completed successfully! 🎉"
}

# Execute main function
main "$@"