# OpenClaw + NcatBot 互通完整教程（可运行示例）

本目录是一个最小可运行示例，只保留 `openclaw` 插件。

## 目录说明

- `main.py`：NcatBot 启动入口（含 `#重载`）
- `config.yaml`：NcatBot 配置
- `commands.json`：最小命令配置
- `plugins/openclaw/`：OpenClaw 插件

## 操作步骤说明

若没有下载docker请先自行下载[Docker](https://www.docker.com/)，并配置 `docker` 命令，如果是docker-desktop，记得要在设置中开启enable host networking选项，位于设置-source-network里面

1. 运行命令
   1. 如果你是 Unix：
      ```bash
      docker run -it --network host -v ./:/root/workdir -w /root/workdir docker.1ms.run/ubuntu:22.04
      ```
   2. 如果你是 Windows（PowerShell）：
      ```powershell
      docker run -it --network host -v "${PWD}:/root/workdir" -w /root/workdir docker.1ms.run/ubuntu:22.04
      ```
2. 下载 node.js 与 npm
  ```bash
  apt-get update

  apt install curl git sudo wget

  curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash

  \. "$HOME/.nvm/nvm.sh"

  nvm install 24

  node -v

  npm -v
  ```

3. 下载 openclaw
  ```bash
  npm i -g openclaw

  openclaw onboard
  ```

4. 先安装 conda（按架构自动选择安装包）
  ```bash
  # 下载 miniconda、全输入 yes
  ARCH="$(uname -m)"
  if [ "$ARCH" = "x86_64" ]; then
    CONDA_PKG="Miniconda3-latest-Linux-x86_64.sh"
  elif [ "$ARCH" = "aarch64" ] || [ "$ARCH" = "arm64" ]; then
    CONDA_PKG="Miniconda3-latest-Linux-aarch64.sh"
  else
    echo "不支持的架构: $ARCH"
    exit 1
  fi

  wget "https://repo.anaconda.com/miniconda/${CONDA_PKG}"
  bash "./${CONDA_PKG}"
  ```

5. 然后刷新文件配置
  ```bash
  source ~/.bashrc
  ```

6. 运行 openclaw 后端
  ```bash
  nohup openclaw gateway > ./openclaw.log 2>&1 &
  ```

7. 创建 python 环境（第一次创建环境可能需要按两次回车）
  ```bash
  conda create -n qq python=3.11
  ```

8. 激活该环境并下载对应包
  ```bash
  conda activate qq

  sudo apt-get update -y -qq && sudo apt-get -y -qq install curl sudo

  pip install ncatbot -U -i https://mirrors.aliyun.com/pypi/simple

  pip install PyYaml
  ```

9. 修改文件配置 `config.yaml`，root 用户为自己大号，bt_uin 为小号也就是机器人，webui的token。

10. 修改 openclaw 配置，填入 root 用户账号 root_ids 、token、需要机器人聊天的群聊 group_pool。

11. 运行 ncatbot 后端
  ```bash
  # 安装napcat
  curl -o napcat.sh https://nclatest.znin.net/NapNeko/NapCat-Installer/main/script/install.sh

  bash napcat.sh --docker n --cli y --proxy 0
  # 第一次需要扫码登录QQ
  python main.py
  # 然后后台运行
  nohup python main.py > ./ncatbot.log 2>&1 &
  ```

## 致谢
  - [ncatbot](https://docs.ncatbot.xyz/)-简洁高效的QQ机器人python框架
  - [openclaw](https://openclaw.ai/)-可集成多模型的自动化机器人
  - [Napcat](https://napneko.github.io/)-强大的QQ协议实现与消息收发服务
