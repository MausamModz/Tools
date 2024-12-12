<div align="center">
  <h1 align="center">Dex2C</h1>  
  <p align="center">
    Method-based AOT compiler that can wrap Dalvik bytecode with JNI native code.
  </p>
</div>

### Requierements
1. Python3
2. lxml python package.
   ```bash
   pkg install python-lxml
   ```
3. JRE/JDK
3. Android NDK

### Installation
   ```bash
   git clone https://github.com/MausamModz/Tools/tree/main/dex2c
   ```
- configure dcc.cfg with your NDK path

<!-- USAGE EXAMPLES -->
# Usage

### Filters

Add all your filters in `filter.txt` file - one rule for each line. Filters are made using regex patterns. There are two types of filters available in **Dex2c** - whitelist, and blacklist. You can use them whenever you need them.

#### WhiteList

- Protect just one method in a specific class.
```
com/some/class;some_method(some_parameters)return_type
```

- Protect all methods in a specific class.
```
com/some/class;.*
```

- Protect all methods in all classes under a package path.
```
com/some/package/.*;.*
```

- Protect a method with the name onCreate in all classes.
```
.*;onCreate\(.*
```

#### BlackList

Adding an exclamation `!` sign before a rule will mark that rule as a blacklist.

- Exclude one method in a specific class from being protected.
```
!com/some/class;some_method(some_parameters)return_type
```

- Exclude all methods in a specific class from being protected.
```
!com/some/class;.*
```

- Exclude all methods in all classes under a package path from being protected.
```
!com/some/package/.*;.*
```

- Exclude a method with the name onCreate in all classes from being protected.
```
!.*;onCreate\(.*
```


### Protect apps

- Copy your apk file to `dex2c` folder where `dcc.py` is located and run this command.

```bash
python3 dcc.py -a input.apk --custom-loader -o output.apk
```

- Run this command to know about all the other options available in dcc to find the best ones for your needs.

```bash
python3 dcc.py --help
```

### Major updates
- changed <a href="https://apktool.org/">Apktool</a> for <a href="https://github.com/REAndroid/APKEditor">APKEditor</a>
- cleaned androguard from useless parts and removed dependencies
- DEX file support: creates a ZIP archive of the built libraries and dex file
- skip constructors by default
- the application class is the loader ; if not defined or absent from dex, the custom loader is used
- --allow-init option: do not skip constructors
- --lib-name option: edit the library name, default: stub
- --output default value is « output.apk » for an APK else « output.zip » for a DEX
- --input only is required 
- all options can be configured in dcc.cfg ; options passed to the command line have priority
- adjust APP_PLATFORM automatically
