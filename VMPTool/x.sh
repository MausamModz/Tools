#!/bin/sh
GREEN='\033[1;32m'
RED='\033[1;31m'
YELLOW='\033[1;33m'
BLUE='\033[1;34m'
CYAN='\033[1;36m'
PURPLE='\033[1;35m'
WHITE='\033[1;37m'
NC='\033[0m'

SPINNER="⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
LOADING_BAR="▰▱"
BASE_DIR=$(cd "$(dirname "$0")" && pwd)
OUO_DIR="$BASE_DIR/OuO"
Tool_DIR="$OUO_DIR/tool"

show_title() {
    clear
    echo -ne "\n"
    echo -e "${RED}╔════════════════════════════════════════╗${NC}"
    echo -e "${RED}║${NC}              ${CYAN}D${PURPLE}e${YELLOW}x${GREEN}V${RED}M${BLUE}P${NC} ${WHITE}Tool${NC}               ${RED}║${NC}"
    echo -e "${RED}╚════════════════════════════════════════╝${NC}"
    sleep 1
}

show_loading_bar() {
    local duration=$1
    local width=30
    echo -ne "\n"
    for i in $(seq 0 $width); do
        progress=$(expr $i \* 100 / $width)
        printf "\r${PURPLE}[${NC}"
        for j in $(seq 0 $((width - 1))); do
            if [ $j -lt $i ]; then
                printf "${GREEN}${LOADING_BAR:0:1}${NC}"
            else
                printf "${WHITE}${LOADING_BAR:1:1}${NC}"
            fi
        done
        printf "${PURPLE}]${NC} ${YELLOW}%d%%${NC}" $progress
        sleep $(echo "scale=2; $duration/$width" | bc)
    done
    echo -ne "\n"
}

show_title

echo -e "\n${PURPLE}🔧 Configuring environment variables...${NC}"
package_path=$(echo $PREFIX | awk -F'/files' '{print $1}')
export ANDROID_HOME=$(find "$package_path" -type f -name "ndk-build" -o -name "build-ndk" 2>/dev/null | head -n 1 | awk -F'/ndk/' '{print $1}')
export ANDROID_NDK_ROOT=$(find "$ANDROID_HOME/ndk" -maxdepth 1 -type d | grep -E '/ndk/+' | sort -V | tail -n 1)
export ANDROID_SDK_HOME="$ANDROID_HOME"
export ANDROID_NDK_HOME="$ANDROID_NDK_ROOT"
export CMAKE_PATH="$ANDROID_SDK_HOME/cmake/3.25.1/"
export PATH=$PATH:"$CMAKE_PATH":"$NDK_PATH":"$ANDROID_SDK_HOME":"ANDROID_NDK_HOME"
export SDK_PATH="$ANDROID_HOME"
export NDK_PATH="$ANDROID_NDK_ROOT"
echo -e "${GREEN}✓ Environment variables configured${NC}"
echo -e "\n${PURPLE}📝 Checking necessary files...${NC}"
if [ ! -f "$Tool_DIR/vm-protect.jar" ] || [ ! -f "$Tool_DIR/convertRules.txt" ] || [ ! -f "$Tool_DIR/mapping.txt" ]; then
    echo -e "\n${RED}Missing required files!${NC}"
    echo -e "${YELLOW}Please ensure the following files exist: OuO/vm-protect.jar, OuO/convertRules.txt, OuO/mapping.txt${NC}"
    exit 1
else
    echo -e "${GREEN}✓ File check passed${NC}"
fi
APK_FILE=$(find "$BASE_DIR" -maxdepth 1 -name "*.apk" | head -n 1)
if [ -z "$APK_FILE" ]; then
    echo -e "\n${RED}No APK file found!${NC}"
    exit 1
else
    APK_BASENAME=$(basename "$APK_FILE")
    echo -e "${GREEN}✓ Found APK file: ${CYAN}$APK_BASENAME${NC}"
fi
echo -e "\n${PURPLE}🚀 Compiling...${NC}"
show_loading_bar 3
java -jar "$Tool_DIR/vm-protect.jar" apk "$APK_FILE" "$Tool_DIR/convertRules.txt" "$Tool_DIR/mapping.txt" > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Compilation successful${NC}"
else
    echo -e "${RED}✗ Compilation failed${NC}"
    exit 1
fi
echo -e "\n${PURPLE}🛡️ Protecting...${NC}"
show_loading_bar 2
PROTECTED_APK_FILE="$BASE_DIR/build/${APK_BASENAME%.apk}-protect.apk"
while [ ! -f "$PROTECTED_APK_FILE" ]; do
    for i in $(seq 0 7); do
        printf "\r${YELLOW}[${NC}${CYAN}Protecting${NC}${YELLOW}]${NC} ${CYAN}${SPINNER:$i:1}${NC}"
        sleep 0.1
    done
done
echo -e "${GREEN}✓ Protection successful${NC}"
echo -e "\n${PURPLE}📦 Outputting protected file...${NC}"
cp "$PROTECTED_APK_FILE" "$BASE_DIR/vm-protect.apk"
echo -e "${GREEN}✓ Output complete${NC}"
echo -e "\n${PURPLE}🔏 Skipping APK signing.${NC}"
echo -e "\n${PURPLE}🧹 Cleaning temporary files...${NC}"
rm -rf "$BASE_DIR/tools" "$Tool_DIR/tools" "$BASE_DIR/build" "$BASE_DIR/dexvm-protect.apk"
show_loading_bar 2
echo -e "${GREEN}✓ Cleanup complete${NC}"
echo -e "\n${RED}╔════════════════════════════════════════╗${NC}"
echo -e "${RED}║${NC}     ${GREEN}✨App successfully encrypted✨${NC}${RED}     ║${NC}"
echo -e "${RED}╚════════════════════════════════════════╝${NC}"