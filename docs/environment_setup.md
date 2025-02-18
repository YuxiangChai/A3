# Environment Setup

## For Linux/Mac

### 1. Install Node.js

- Install `nvm` from [link](https://github.com/nvm-sh/nvm?tab=readme-ov-file#install--update-script)

- Install `node` and `npm` by `nvm` from [link](https://github.com/nvm-sh/nvm?tab=readme-ov-file#usage)

### 2. Install Appium Server

official website: [link](https://appium.io/docs/en/2.4/quickstart/install/)

### 3. Setup requirements for UIAutomator2 Driver

- Install JDK from [link](https://www.oracle.com/java/technologies/downloads/)
- Add `JAVA_HOME` to the environment variable. In Linux or Mac, add the following line to `~/.bashrc` or `~/.zshrc`:

  ```shell
  export JAVA_HOME="/path/to/jdk"
  ```

- Install Android Studio from [link](https://developer.android.com/studio), use default settings to install.
- Add `ANDROID_HOME` to the environment variable. In Linux or Mac, add the following line to `~/.bashrc` or `~/.zshrc`:

  ```shell
  export ANDROID_HOME="/path/to/Android/Sdk"
  ```

- Add `platform-tools` and `build-tools` to the `PATH` environment variable. In Linux or Mac, add the following line to `~/.bashrc` or `~/.zshrc`:

  ```shell
  export PATH=$PATH:$ANDROID_HOME/platform-tools
  ```

example:

```shell
export ANDROID_HOME="/home/<user>/Android/Sdk/"
export JAVA_HOME="/usr/lib/jvm/jdk-21-oracle-x64/"
export "PATH=${PATH}:/home/<user>/Android/Sdk/build-tools/34.0.0/"
export "PATH=${PATH}:/home/<user>/Android/Sdk/platform-tools/"
```

### 4. Install Appium Driver

In terminal run

```shell
appium driver install uiautomator2
```

### 5. Create Android Virtual Device (AVD) and run

#### Option 1: Use Android Studio

Follow the official guide [link](https://developer.android.com/studio/run/managing-avds) and notice:

- Use Pixel 7 pro / Pixel 7 / Pixel 6
- Use Android 11/12/13 system image
- Set internal storage to 10240 MB in the advanced settings

Then run the AVD.

#### Option 2: Use Genymotion

Follow the official guide [link](https://www.genymotion.com/product-desktop/) and notice:

- Free trial / personal version is enough
- Use whatever device you like
- Use Android 11/12/13 system image

### 6. Install Appium client

In terminal run

```shell
conda create -n avd python=3.10
conda activate avd
pip install -r requirements.txt
```

## For Windows

### 1. Install Node.js

1. install `nvm-windows` from [link](https://github.com/coreybutler/nvm-windows)
2. install `node` and `npm` by `nvm-windows` from [link](https://github.com/coreybutler/nvm-windows?tab=readme-ov-file#usage)

### 2. Install Appium Server

official website: [link](https://appium.io/docs/en/2.4/quickstart/install/)

### 3. Setup requirements for UIAutomator2 Driver

- Install JDK from [link](https://www.oracle.com/java/technologies/downloads/)
- Add `JAVA_HOME` to the environment variable. Your can follow the guide from [link](https://windowsloop.com/add-environment-variable-in-windows-10/). The path should be something like `C:\Program Files\Java\jdk-21`
- Install Android Studio from [link](https://developer.android.com/studio), use default settings to install.
- Add `ANDROID_HOME` to the environment variable. The path should be something like `C:\Users\<user>\AppData\Local\Android\Sdk`, which can be checked from Android Studio -> Settings -> SDK Manager.

### 4. Install Appium Driver

```shell
appium driver install uiautomator2
```

### 5. Create Android Virtual Device (AVD) and run

#### Option 1: Use Android Studio

Follow the official guide [link](https://developer.android.com/studio/run/managing-avds) and notice:

- Use Pixel 7 pro / Pixel 7 / Pixel 6
- Use Android 11/12/13 system image
- Set internal storage to 10240 MB in the advanced settings

Then run the AVD.

#### Option 2: Use Genymotion

Follow the official guide [link](https://www.genymotion.com/product-desktop/) and notice:

- Free trial / personal version is enough
- Use whatever device you like
- Use Android 11/12/13 system image

### 6. Install Appium client

In terminal run

```shell
conda create -n avd python=3.10
conda activate avd
pip install -r requirements.txt
```
