# Makefile for Order Book Analysis

CXX = g++
CXXFLAGS = -std=c++17 -O3 -Wall -Wextra
TARGET = order_book_analysis
SOURCE = order_book_analysis.cpp

# Default target
all: $(TARGET)

# Compile the main program
$(TARGET): $(SOURCE)
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(SOURCE)

# Clean build artifacts
clean:
	rm -f $(TARGET) $(TARGET).exe *.csv

# Run the analysis
run: $(TARGET)
	./$(TARGET)

# For Windows (if using MinGW)
windows: $(SOURCE)
	g++ -std=c++17 -O3 -Wall -Wextra -o $(TARGET).exe $(SOURCE)

# Debug version
debug: $(SOURCE)
	$(CXX) -std=c++17 -g -Wall -Wextra -o $(TARGET)_debug $(SOURCE)

.PHONY: all clean run windows debug
