<a name="readme-top"></a>

<div align="center">
  <h1 align="center">DEXVMPTool</h1>

## Need to do


```
apt update && apt upgrade -y && pkg update && pkg upgrade -y && pkg install openjdk-17 -y && pkg install bc -y
```


# Usage

### Filters
In the `convertRules.txt` define rules to obfuscate specific classes and methods within a project. Here’s how each rule works:


- This rule obfuscates all classes in the com.example package and all methods within those classes.

```
class com.example.* { *; }
```


- This rule targets the application class in the com.example package, obfuscating all methods within that specific class.

```
class com.example.application { *; }
```


- This rule is more specific: it applies to the application class in the com.example package but limits obfuscation to method1 and method2 only.

```
class com.example.application { method1; method2; }
```


  
## install the Android NDK offline in Termux
- using the `android-ndk-aarch64.zip` file you’ve already downloaded, follow these steps:

- Steps to Install Android NDK Offline in Termux
Move to the desired directory: First, move the downloaded `android-ndk-aarch64.zip` to the directory where you want to install the NDK (for example, in your home directory).

- If the file is in your Downloads folder, you can move it to your home directory or any other location you prefer:

```
mv ~/storage/downloads/android-ndk-aarch64.zip ~/
```

- Install unzip: Ensure that unzip is installed on your Termux if you don't have it already.

```
pkg install unzip
```

- Extract the NDK: Navigate to the directory where you moved the zip file and unzip it.

```
cd ~unzip android-ndk-aarch64.zip
```

- This will extract the contents of the zip file into a directory named android-ndk (or similar).

- Add NDK to your PATH: To use the NDK from any directory, add the extracted NDK directory to your PATH environment variable.

- Open your `.bashrc or .zshrc`(depending on the shell you're using) to edit the file.

```
nano ~/.bashrc
```

or

```
nano ~/.zshrc
```  

- Add the following line to include the NDK directory in your PATH `(replace ~/android-ndk with the correct path if different)`:


```
export PATH=$PATH:/data/data/com.termux/files/home/android-sdk/ndk/27.1.12297006
export PATH=$PATH:/data/data/com.termux/files/home/android-sdk/build-tools/34.0.4
export PATH=$PATH:/data/data/com.termux/files/home/android-sdk/cmdline-tools/latest/bin
```


- Save and close the file. If you're using nano, press CTRL + X, then Y, and then Enter.

- Source the file: To apply the changes to your current session, source the `.bashrc or .zshrc file`:

```
source ~/.bashrc
``` 

or

```
source ~/.zshrc
``` 


- Verify the installation: To check if the NDK was installed correctly, run:


```
ndk-build --version
```

If everything is set up correctly, you should see the version of the Android NDK printed out. If not give executable permission `PATH/TO/YOURFILES/`


```
chmod +x /data/data/com.termux/files/home/android-sdk/cmake/3.25.1/bin/cmake
chmod -R 755 /data/data/com.termux/files/home/android-sdk/cmake/3.25.1/bin
chmod +x /data/data/com.termux/files/home/android-sdk/ndk/27.1.12297006/build/cmake/android.toolchain.cmake
chmod +x /data/data/com.termux/files/home/android-sdk/build-tools/34.0.4/aapt2
```
