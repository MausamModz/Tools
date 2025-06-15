import os
import sys
import shutil
import re
import subprocess
import glob
import platform
from pathlib import Path
import time

# Auto-install required packages
def install_dependencies():
    """Install required dependencies if not present"""
    try:
        # Define needed packages
        required_packages = []  # Removed colorama and tqdm
        
        # Check if pip is available
        try:
            import pip
        except ImportError:
            print("Installing pip...")
            # For Windows
            if platform.system() == "Windows":
                subprocess.run([sys.executable, "-m", "ensurepip", "--upgrade"], 
                              check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # For Unix-like systems
            else:
                try:
                    # Try using get-pip.py
                    import urllib.request
                    print("Downloading get-pip.py...")
                    urllib.request.urlretrieve("https://bootstrap.pypa.io/get-pip.py", "get-pip.py")
                    subprocess.run([sys.executable, "get-pip.py", "--user"], 
                                  check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    os.remove("get-pip.py")
                except Exception as e:
                    print(f"Failed to install pip: {e}")
                    print("Please install pip manually and try again.")
                    sys.exit(1)
        
        # Now check for required packages and install them
        for package in required_packages:
            try:
                __import__(package)
            except ImportError:
                print(f"Installing {package}...")
                subprocess.run([sys.executable, "-m", "pip", "install", "--user", package], 
                              check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Restart script after installing dependencies
        print("Dependencies installed successfully. Restarting script...")
        if platform.system() == "Windows":
            os.system("cls")
        else:
            os.system("clear")
        os.execv(sys.executable, [sys.executable] + sys.argv)
        
    except Exception as e:
        print(f"Error installing dependencies: {e}")
        sys.exit(1)

class Logger:
    """Simple logger for terminal output"""
    def __init__(self):
        pass
    
    def info(self, message):
        """Print info message"""
        print(f"[i] {message}")
    
    def success(self, message):
        """Print success message"""
        print(f"[✓] {message}")
    
    def error(self, message):
        """Print error message"""
        print(f"[✗] {message}")
    
    def warning(self, message):
        """Print warning message"""
        print(f"[!] {message}")
    
    def header(self, message):
        """Print header message"""
        print(f"\n▶ {message}")
    
    def subheader(self, message):
        """Print subheader message"""
        print(f"  ➤ {message}")

# Create global logger
log = Logger()

def run_command(command, verbose=False, exit_on_error=True):
    """Run a shell command and return output"""
    if verbose:
        log.info(f"Running: {command}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            log.error(f"Command failed with error code {result.returncode}")
            if verbose:
                log.error(f"STDERR: {result.stderr}")
            if exit_on_error:
                sys.exit(1)
        return result.stdout.strip()
    except Exception as e:
        log.error(f"Exception while executing command: {e}")
        if exit_on_error:
            sys.exit(1)
        return ""

def extract_file(zipfile, target=None):
    """Extract file from zip archive using platform-appropriate method"""
    try:
        if platform.system() == "Windows":
            # Try using 7z if available
            if shutil.which("7z"):
                run_command(f'7z e "{zipfile}" {target or ""} -y -o.', verbose=False)
            else:
                # Fallback to Python's zipfile module
                import zipfile as zf
                with zf.ZipFile(zipfile, 'r') as zip_ref:
                    if target:
                        zip_ref.extract(target)
                    else:
                        zip_ref.extractall()
        else:
            # Use unzip on Unix-like systems
            if shutil.which("unzip"):
                result = run_command(f'unzip -o "{zipfile}" {target or ""}', verbose=False, exit_on_error=False)
                log.info(f"Unzip result: {result}")
                if not os.path.exists(target or ''):
                    log.error(f"Extracted file not found after unzip")
            else:
                import zipfile as zf
                with zf.ZipFile(zipfile, 'r') as zip_ref:
                    if target:
                        zip_ref.extract(target)
                    else:
                        zip_ref.extractall()
        return True
    except Exception as e:
        log.error(f"Failed to extract {target or 'files'} from {zipfile}: {e}")
        return False

def delete_dir_crossplatform(path):
    """Delete directory or file cross-platform"""
    try:
        if os.path.isfile(path):
            os.remove(path)
            return True
        elif os.path.isdir(path):
            if platform.system() == "Windows":
                os.system(f'rmdir /s /q "{path}" > nul 2>&1')
            else:
                os.system(f'rm -rf "{path}" > /dev/null 2>&1')
            return True
        return False
    except Exception as e:
        log.warning(f"Failed to delete {path}: {e}")
        return False

def patch_files():
    """Apply patches to the decompiled files"""
    base_dir = os.path.expanduser('merged_app_decompile_xml')
    base_lib_dir = os.path.join(base_dir, 'root/lib')
    resources_dir = os.path.join(base_dir, 'resources')
    cwd = os.getcwd()
    
    log.header("Applying patches to decompiled files")

    # --- Replacement for VMRunner.clinit()
    new_clinit_block = [
    ".method static constructor <clinit>()V",
    "    .registers 4",
    "",
    "    .line 30",
    "",
    "    const/4 v0, 0x5",
    "",
    "    new-array v0, v0, [C",
    "",
    "    fill-array-data v0, :array_5",
    "",
    "    invoke-static {v0}, Ljava/lang/String;->valueOf([C)Ljava/lang/String;",
    "",
    "    move-result-object v2",
    "",
    "    invoke-static {v2}, Ljava/lang/System;->loadLibrary(Ljava/lang/String;)V",
    "",
    "    const/16 v1, 0xA",
    "",
    "    new-array v1, v1, [C",
    "",
    "    fill-array-data v1, :array_10",
    "",
    "    invoke-static {v1}, Ljava/lang/String;->valueOf([C)Ljava/lang/String;",
    "",
    "    move-result-object v2",
    "",
    "    invoke-static {v2}, Ljava/lang/System;->loadLibrary(Ljava/lang/String;)V",
    "",
    "    return-void",
    "",
    "    :array_5",
    "    .array-data 2",
    "        0x66  ",
    "        0x75  ",
    "        0x63  ",
    "        0x6b  ",
    "        0x70  ",
    "    .end array-data",
    "",
    "    :array_10",
    "    .array-data 2",
    "        0x70  ",
    "        0x61  ",
    "        0x69  ",
    "        0x72  ",
    "        0x69  ",
    "        0x70  ",
    "        0x63  ",
    "        0x6f  ",
    "        0x72  ",
    "        0x65  ",
    "    .end array-data",
    ".end method"
]

    # --- Patch Smali Files ---
    log.subheader("Patching protection code...")
    vmrunner_patched = False
    sigcheck_patched = False
    
    for root, dirs, files in os.walk(base_dir):
        # --- Patch VMRunner.smali ---
        if os.path.basename(root) == 'pairip' and 'VMRunner.smali' in files:
            vmrunner_path = os.path.join(root, 'VMRunner.smali')
            with open(vmrunner_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            new_lines = []
            inside_clinit = False
            method_start_found = False

            for line in lines:
                if not inside_clinit and line.strip().startswith('.method') and '<clinit>()V' in line:
                    inside_clinit = True
                    method_start_found = True
                    new_lines.extend(line + '\n' for line in new_clinit_block)
                    continue

                if inside_clinit:
                    if line.strip() == '.end method':
                        inside_clinit = False
                    continue

                new_lines.append(line)

            if method_start_found:
                with open(vmrunner_path, 'w', encoding='utf-8') as f:
                    f.writelines(new_lines)
                log.success('Patched VMRunner.smali')
                vmrunner_patched = True

        # --- Patch SignatureCheck.smali ---
        if os.path.basename(root) == 'pairip' and 'SignatureCheck.smali' in files:
            sig_path = os.path.join(root, 'SignatureCheck.smali')
            with open(sig_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            new_lines = []
            inside_verify = False
            annotation_ended = False
            method_found = False

            for i, line in enumerate(lines):
                stripped = line.strip()

                if not inside_verify and stripped.startswith('.method') and 'verifyIntegrity(Landroid/content/Context;)V' in stripped:
                    inside_verify = True
                    method_found = True

                if inside_verify and not annotation_ended and stripped == '.end annotation':
                    annotation_ended = True
                    new_lines.append(line)
                    if not any('return-void' in l for l in lines[i+1:i+5]):
                        new_lines.append('    return-void\n')
                    continue

                new_lines.append(line)

            if method_found:
                with open(sig_path, 'w', encoding='utf-8') as f:
                    f.writelines(new_lines)
                log.success('Patched SignatureCheck.smali')
                sigcheck_patched = True

    if not vmrunner_patched:
        log.warning('VMRunner.smali not found or not patched')
    if not sigcheck_patched:
        log.warning('SignatureCheck.smali not found or not patched')

    # --- Copy .so Files ---
    log.subheader("Copying native libraries...")
    so_files_to_copy = [
        'libfuckp.so',
        'libFirebaseCppApp.so'
    ]

    missing = [f for f in so_files_to_copy if not os.path.exists(os.path.join(cwd, f))]
    if missing:
        log.error(f"Missing files in current directory: {', '.join(missing)}")
        sys.exit(1)
    else:
        lib_dirs_found = 0
        arch_types = []
        for root, dirs, files in os.walk(base_lib_dir):
            if 'libpairipcore.so' in files:
                arch_type = os.path.basename(root)
                arch_types.append(arch_type)
                lib_dirs_found += 1
                for so_file in so_files_to_copy:
                    src_path = os.path.join(cwd, so_file)
                    dst_path = os.path.join(root, so_file)
                    shutil.copy2(src_path, dst_path)
                    log.success(f'Copied {so_file} to {arch_type} architecture')
        
        if lib_dirs_found == 0:
            log.warning("No library directories found containing libpairipcore.so")
        else:
            log.success(f"Libraries copied to {lib_dirs_found} architecture(s): {', '.join(arch_types)}")

    # --- Patch file_paths.xml in resources/*/res/xml/
    log.subheader("Patching file paths configuration...")
    file_paths_patched = 0
    pattern = re.compile(
        r'<external-path\s+name="[^"]*"\s+path="Android/data/[^"]*/files/Pictures"\s*/>',
        re.IGNORECASE
    )
    replacement = '<external-files-path name="my_images" path="Pictures/" />'

    for root, dirs, files in os.walk(resources_dir):
        if 'file_paths.xml' in files and 'res/xml' in root:
            xml_path = os.path.join(root, 'file_paths.xml')
            with open(xml_path, 'r', encoding='utf-8') as f:
                content = f.read()

            if pattern.search(content):
                content_new = pattern.sub(replacement, content)
                with open(xml_path, 'w', encoding='utf-8') as f:
                    f.write(content_new)
                file_paths_patched += 1

    if file_paths_patched > 0:
        log.success(f"Patched {file_paths_patched} file_paths.xml file(s)")
    else:
        log.warning("No matching <external-path> entries found")

    return vmrunner_patched or sigcheck_patched

def process_apk(apks_file):
    """Process an APKS file"""
    # Check if required JAR files exist
    required_jars = ["APKEditor.jar"]  # Removed signing requirement
    for jar in required_jars:
        if not os.path.exists(jar):
            log.error(f"Required JAR file '{jar}' not found")
            sys.exit(1)

    # Get the base name of the APKS file without extension
    base_name = os.path.basename(apks_file).rsplit('.', 1)[0]
    decompile_dir = os.path.expanduser("merged_app_decompile_xml")
    
    # Set Java memory options for large APKs
    if "_JAVA_OPTIONS" not in os.environ:
        os.environ["_JAVA_OPTIONS"] = os.environ.get("_JAVA_OPTIONS", "") + " -Xmx2g"
    
    # Step 1: Extract base.apk
    log.header("Step 1/9: Extracting base.apk")
    extract_file(apks_file, "base.apk")
    
    # Step 2: Create libFirebaseCppApp.so
    log.header("Step 2/9: Creating libFirebaseCppApp.so")
    shutil.copy("base.apk", "libFirebaseCppApp.so")
    log.success("Created libFirebaseCppApp.so from base.apk")
    
    # Step 3: Remove old merged_app.apk if exists
    log.header("Step 3/9: Cleaning previous files")
    cleaned = 0
    if os.path.exists("merged_app.apk"):
        os.remove("merged_app.apk")
        cleaned += 1
    if os.path.exists("merged_app_decompile_xml"):
        delete_dir_crossplatform("merged_app_decompile_xml")
        cleaned += 1
    log.success(f"Removed {cleaned} old files/directories")
    
    # Step 4: Merge APKS to APK
    log.header("Step 4/9: Merging APKS to APK")
    run_command(f'java -jar APKEditor.jar m -i "{apks_file}" -o merged_app.apk -extractNativeLibs true', verbose=False)
    if os.path.exists("merged_app.apk"):
        merged_size = os.path.getsize("merged_app.apk") / (1024 * 1024)  # Size in MB
        log.success(f"Successfully merged to APK (Size: {merged_size:.2f} MB)")
    else:
        log.error("Failed to merge APKS to APK")
        sys.exit(1)
    
    # Step 5: Remove old decompiled directory if exists
    log.header("Step 5/9: Preparing decompilation")
    if os.path.exists(decompile_dir):
        log.info("Removing existing decompiled directory")
        shutil.rmtree(decompile_dir, ignore_errors=True)
    
    # Step 6: Decompile the merged APK
    log.header("Step 6/9: Decompiling merged APK")
    log.info("This may take several minutes depending on APK size...")
    start_time = time.time()
    run_command("java -jar APKEditor.jar d -i merged_app.apk", verbose=False)
    elapsed_time = time.time() - start_time
    
    if os.path.exists(decompile_dir):
        log.success(f"Decompilation completed in {elapsed_time:.1f} seconds")
    else:
        log.error("Decompilation failed")
        sys.exit(1)
    
    # Step 7: Modify AndroidManifest.xml
    log.header("Step 7/9: Modifying AndroidManifest.xml")
    manifest_path = os.path.join(decompile_dir, "AndroidManifest.xml")
    
    if os.path.exists(manifest_path):
        with open(manifest_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Use regex to remove license check components
        pattern1 = r'<activity[^>]+com\.pairip\.licensecheck\.LicenseActivity[^<]+/>'
        pattern2 = r'<provider[^>]+com\.pairip\.licensecheck\.LicenseContentProvider[^<]+/>'
        
        entries_removed = 0
        for pattern in [pattern1, pattern2]:
            matches = re.findall(pattern, content, flags=re.DOTALL)
            entries_removed += len(matches)
            content = re.sub(pattern, '', content, flags=re.DOTALL)
        
        if entries_removed > 0:
            with open(manifest_path, 'w', encoding='utf-8') as f:
                f.write(content)
            log.success(f"Removed {entries_removed} license check entries")
        else:
            log.warning("No license check entries found in manifest")
    else:
        log.warning("AndroidManifest.xml not found")
    
    # Step 8: Patch files
    log.header("Step 8/9: Patching decompiled files")
    patch_result = patch_files()
    
    # Step 9: Build APK from decompiled files and rename as final output
    log.header("Step 9/9: Building modified APK")
    if os.path.exists("out.apk"):
        os.remove("out.apk")
    
    log.info("Building APK from modified files...")
    start_time = time.time()
    run_command(f'java -jar APKEditor.jar b -i "{decompile_dir}" -o out.apk', verbose=False)
    elapsed_time = time.time() - start_time
    
    if os.path.exists("out.apk"):
        output_name = f"{base_name}-patched.apk"
        shutil.copy("out.apk", output_name)
        out_size = os.path.getsize(output_name) / (1024 * 1024)  # Size in MB
        log.success(f"Build completed in {elapsed_time:.1f} seconds (Size: {out_size:.2f} MB)")
    else:
        log.error("Failed to build modified APK")
        sys.exit(1)
    
    # Clean up temporary files
    log.subheader("Cleaning up temporary files...")
    cleanup_files = 0
    
    # Find and clean up any temporary files with .tmp extension
    for tmp_file in glob.glob("*.tmp*"):
        try:
            os.remove(tmp_file)
            cleanup_files += 1
        except Exception:
            pass
    
    # Find and clean up any temporary directories created by Java
    for tmp_dir in glob.glob("tmp-*"):
        if os.path.isdir(tmp_dir):
            try:
                shutil.rmtree(tmp_dir, ignore_errors=True)
                cleanup_files += 1
            except Exception:
                pass
    
    log.success(f"Removed {cleanup_files} temporary files/directories")
    
    return output_name

def center_text(text, width):
    return text.center(width)
    
def main():
    """Main function"""
    width = shutil.get_terminal_size().columns
    border = "=" * width

    line1 = center_text("PairIP Protection Remover v1.1", width)
    line2 = center_text("Cross-platform Edition", width)
    footer = center_text("© void.eth", width)

    print(f"\n{border}")
    print(f"{line1}")
    print(f"{line2}")
    print(f"{border}")
    print(f"{footer}\n")
    
    if len(sys.argv) != 2:
        log.error("Usage: python patch.py app.apks")
        sys.exit(1)
    
    apks_file = sys.argv[1]
    if not os.path.exists(apks_file):
        log.error(f"Input file '{apks_file}' not found")
        sys.exit(1)
    
    if not apks_file.endswith('.apks'):
        log.warning(f"Input file doesn't have .apks extension")
    
    # Check Java installation
    log.info("Checking Java installation...")
    try:
        java_version = run_command("java -version", verbose=False, exit_on_error=False)
        if not java_version:
            java_version = run_command("java -version 2>&1", verbose=False, exit_on_error=False)
        log.success("Java detected")
    except Exception:
        log.error("Java not found. Please install Java Runtime Environment")
        sys.exit(1)
    
    # Create working directory if needed
    work_dir = os.path.dirname(os.path.abspath(apks_file))
    os.chdir(work_dir)
    
    log.info(f"Processing file: {os.path.basename(apks_file)}")
    start_time = time.time()
    out_name = process_apk(apks_file)
    total_time = time.time() - start_time
    
    log.header("Finalizing...")
    leftovers = [
        "base.apk", "merged_app.apk", "out.apk", 
        "merged_app_decompile_xml"  # Removed signed APK patterns
    ]
    
    cleanup_count = 0
    for file in leftovers:
        if os.path.exists(file):
            try:
                delete_dir_crossplatform(file)
                cleanup_count += 1
            except Exception:
                pass
    
    if cleanup_count > 0:
        log.success(f"Removed {cleanup_count} leftover files/directories")
                
    if out_name:
        output_path = os.path.abspath(out_name)
        output_size = os.path.getsize(output_path) / (1024 * 1024)  # Size in MB
        
        print(f"\n╔══════════════════════════════════════════════╗")
        print(f"║              PROCESS COMPLETE                ║")
        print(f"╚══════════════════════════════════════════════╝")
        print(f"\n✓ Final APK: {out_name}")
        print(f"✓ Size: {output_size:.2f} MB")
        print(f"✓ Location: {output_path}")
        print(f"✓ Total processing time: {total_time:.1f} seconds\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\nProcess cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        sys.exit(1)