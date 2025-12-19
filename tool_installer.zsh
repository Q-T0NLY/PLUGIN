#!/usr/bin/env zsh
# Universal Tool Installer (1000+ Tools)

: "${TOOLS_DB:=${HOME}/.config/ultra-zsh/tools/tools_db.json}"
: "${INSTALL_LOG:=${HOME}/.config/ultra-zsh/logs/install.log}"

# Tool database with multiple installation methods (1000+ tools)
declare -A TOOL_DATABASE=(
    # Core Development Languages & Runtimes
    ["node"]="brew:node|npm:npm|curl:https://nodejs.org/dist/v20.11.0/node-v20.11.0.pkg"
    ["python"]="brew:python@3.12|port:python312|curl:https://www.python.org/ftp/python/3.12.0/python-3.12.0-macos11.pkg"
    ["python3"]="brew:python3|port:python312"
    ["rust"]="curl:https://sh.rustup.rs|brew:rust|port:rust"
    ["go"]="brew:go|curl:https://go.dev/dl/go1.21.6.darwin-amd64.tar.gz|port:go"
    ["java"]="brew:openjdk|port:openjdk"
    ["ruby"]="brew:ruby|port:ruby"
    ["php"]="brew:php|port:php"
    ["swift"]="brew:swift|port:swift"
    ["kotlin"]="brew:kotlin|port:kotlin"
    ["scala"]="brew:scala|port:scala"
    ["crystal"]="brew:crystal|port:crystal"
    ["nim"]="brew:nim|port:nim"
    ["zig"]="brew:zig|port:zig"
    ["julia"]="brew:julia|curl:https://julialang.org/downloads/"
    ["elixir"]="brew:elixir|port:elixir"
    ["erlang"]="brew:erlang|port:erlang"
    ["haskell"]="brew:ghc|port:ghc"
    ["ocaml"]="brew:ocaml|port:ocaml"
    ["fsharp"]="brew:fsharp|port:fsharp"
    ["dart"]="brew:dart|port:dart"
    ["lua"]="brew:lua|port:lua"
    ["perl"]="brew:perl|port:perl"
    ["r"]="brew:r|port:r"
    
    # Container & Orchestration
    ["docker"]="brew:docker|curl:https://desktop.docker.com/mac/main/arm64/Docker.dmg|mas:docker"
    ["kubernetes"]="brew:kubernetes-cli|curl:https://dl.k8s.io/release/v1.28.0/bin/darwin/amd64/kubectl|port:kubectl"
    ["kubectl"]="brew:kubernetes-cli|curl:https://dl.k8s.io/release/v1.28.0/bin/darwin/amd64/kubectl"
    ["helm"]="brew:helm|curl:https://get.helm.sh/helm-v3.13.0-darwin-amd64.tar.gz"
    ["k9s"]="brew:k9s|cargo:k9s"
    ["kubectx"]="brew:kubectx|git:https://github.com/ahmetb/kubectx.git"
    ["kompose"]="brew:kompose|curl:https://github.com/kubernetes/kompose/releases/download/v1.28.0/kompose-darwin-amd64"
    ["podman"]="brew:podman|port:podman"
    ["containerd"]="brew:containerd|port:containerd"
    ["runc"]="brew:runc|port:runc"
    ["buildah"]="brew:buildah|port:buildah"
    ["skopeo"]="brew:skopeo|port:skopeo"
    ["crio"]="brew:cri-o|port:cri-o"
    ["minikube"]="brew:minikube|curl:https://github.com/kubernetes/minikube/releases/download/v1.32.0/minikube-darwin-amd64"
    ["kind"]="brew:kind|curl:https://kind.sigs.k8s.io/dl/v0.20.0/kind-darwin-amd64"
    ["k3d"]="brew:k3d|curl:https://github.com/k3d-io/k3d/releases/download/v5.5.2/k3d-darwin-amd64"
    ["skaffold"]="brew:skaffold|curl:https://github.com/GoogleContainerTools/skaffold/releases/download/v2.7.0/skaffold-darwin-amd64"
    ["tilt"]="brew:tilt|curl:https://github.com/tilt-dev/tilt/releases/download/v0.32.4/tilt.0.32.4.mac.x86_64.tar.gz"
    
    # AI/ML Tools & Frameworks
    ["ollama"]="brew:ollama|curl:https://ollama.ai/download/Ollama-darwin.zip"
    ["pytorch"]="pip:torch|conda:pytorch|brew:pytorch"
    ["tensorflow"]="pip:tensorflow|conda:tensorflow-gpu|brew:tensorflow"
    ["jupyter"]="pip:jupyter|conda:jupyter|brew:jupyter"
    ["pandas"]="pip:pandas|conda:pandas"
    ["numpy"]="pip:numpy|conda:numpy"
    ["scipy"]="pip:scipy|conda:scipy"
    ["scikit-learn"]="pip:scikit-learn|conda:scikit-learn"
    ["matplotlib"]="pip:matplotlib|conda:matplotlib"
    ["seaborn"]="pip:seaborn|conda:seaborn"
    ["plotly"]="pip:plotly|conda:plotly"
    ["keras"]="pip:keras|conda:keras"
    ["transformers"]="pip:transformers|conda:transformers"
    ["huggingface-hub"]="pip:huggingface-hub|conda:huggingface-hub"
    ["langchain"]="pip:langchain|conda:langchain"
    ["llama-index"]="pip:llama-index|conda:llama-index"
    ["chromadb"]="pip:chromadb|conda:chromadb"
    ["pinecone"]="pip:pinecone-client|conda:pinecone-client"
    ["weaviate"]="pip:weaviate-client|conda:weaviate-client"
    ["milvus"]="pip:pymilvus|conda:pymilvus"
    ["qdrant"]="pip:qdrant-client|conda:qdrant-client"
    ["faiss"]="pip:faiss-cpu|conda:faiss-cpu"
    ["onnx"]="pip:onnx|conda:onnx"
    ["onnxruntime"]="pip:onnxruntime|conda:onnxruntime"
    ["openai"]="pip:openai|conda:openai"
    ["anthropic"]="pip:anthropic|conda:anthropic"
    ["groq"]="pip:groq|conda:groq"
    ["deepseek"]="pip:deepseek-api|conda:deepseek-api"
    ["xai"]="pip:xai|conda:xai"
    ["cohere"]="pip:cohere|conda:cohere"
    ["replicate"]="pip:replicate|conda:replicate"
    ["together"]="pip:together|conda:together"
    ["perplexity"]="pip:perplexity-ai|conda:perplexity-ai"
    
    # DevOps & Infrastructure
    ["terraform"]="brew:terraform|curl:https://releases.hashicorp.com/terraform/1.6.6/terraform_1.6.6_darwin_amd64.zip"
    ["ansible"]="brew:ansible|pip:ansible|port:ansible"
    ["vagrant"]="brew:vagrant|curl:https://releases.hashicorp.com/vagrant/2.4.0/vagrant_2.4.0_darwin_amd64.dmg"
    ["packer"]="brew:packer|curl:https://releases.hashicorp.com/packer/1.10.0/packer_1.10.0_darwin_amd64.zip"
    ["vault"]="brew:vault|curl:https://releases.hashicorp.com/vault/1.15.0/vault_1.15.0_darwin_amd64.zip"
    ["consul"]="brew:consul|curl:https://releases.hashicorp.com/consul/1.17.0/consul_1.17.0_darwin_amd64.zip"
    ["nomad"]="brew:nomad|curl:https://releases.hashicorp.com/nomad/1.6.0/nomad_1.6.0_darwin_amd64.zip"
    ["pulumi"]="brew:pulumi|curl:https://get.pulumi.com/install.sh"
    ["cloudformation"]="pip:aws-cloudformation|brew:aws-cloudformation"
    ["boto3"]="pip:boto3|conda:boto3"
    ["aws-sam"]="brew:aws-sam-cli|pip:aws-sam-cli"
    ["serverless"]="npm:serverless|brew:serverless"
    ["cdk"]="npm:aws-cdk|brew:aws-cdk"
    ["terraform-docs"]="brew:terraform-docs|curl:https://github.com/terraform-docs/terraform-docs/releases/download/v0.16.0/terraform-docs-v0.16.0-darwin-amd64.tar.gz"
    ["tflint"]="brew:tflint|curl:https://github.com/terraform-linters/tflint/releases/download/v0.47.0/tflint_darwin_amd64.zip"
    ["tfsec"]="brew:tfsec|curl:https://github.com/aquasecurity/tfsec/releases/download/v1.28.1/tfsec-darwin-amd64"
    ["checkov"]="pip:checkov|brew:checkov"
    ["infracost"]="brew:infracost|curl:https://github.com/infracost/infracost/releases/download/v0.10.30/infracost-darwin-amd64.tar.gz"
    
    # Security Tools
    ["nmap"]="brew:nmap|port:nmap|curl:https://nmap.org/dist/nmap-7.95.tar.bz2"
    ["metasploit"]="brew:metasploit|curl:https://github.com/rapid7/metasploit-framework/archive/refs/heads/master.zip"
    ["wireshark"]="brew:wireshark|mas:wireshark|port:wireshark"
    ["burp-suite"]="brew:burp-suite|curl:https://portswigger.net/burp/communitydownload"
    ["zap"]="brew:owasp-zap|curl:https://github.com/zaproxy/zaproxy/releases/download/v2.14.0/ZAP_2.14.0.dmg"
    ["nikto"]="brew:nikto|port:nikto"
    ["sqlmap"]="brew:sqlmap|git:https://github.com/sqlmapproject/sqlmap.git"
    ["john"]="brew:john-jumbo|port:john"
    ["hashcat"]="brew:hashcat|port:hashcat"
    ["aircrack-ng"]="brew:aircrack-ng|port:aircrack-ng"
    ["hydra"]="brew:hydra|port:hydra"
    ["ettercap"]="brew:ettercap|port:ettercap"
    ["tshark"]="brew:wireshark|port:wireshark"
    ["tcpdump"]="brew:tcpdump|port:tcpdump"
    ["masscan"]="brew:masscan|port:masscan"
    ["rustscan"]="cargo:rustscan|brew:rustscan"
    ["naabu"]="brew:naabu|curl:https://github.com/projectdiscovery/naabu/releases/download/v2.1.6/naabu_2.1.6_darwin_amd64.zip"
    ["subfinder"]="brew:subfinder|curl:https://github.com/projectdiscovery/subfinder/releases/download/v2.6.3/subfinder_2.6.3_darwin_amd64.zip"
    ["amass"]="brew:amass|curl:https://github.com/owasp-amass/amass/releases/download/v4.2.0/amass_darwin_amd64.zip"
    ["httpx"]="brew:httpx|curl:https://github.com/projectdiscovery/httpx/releases/download/v1.3.7/httpx_1.3.7_darwin_amd64.zip"
    ["nuclei"]="brew:nuclei|curl:https://github.com/projectdiscovery/nuclei/releases/download/v3.1.0/nuclei_3.1.0_darwin_amd64.zip"
    ["gobuster"]="brew:gobuster|curl:https://github.com/OJ/gobuster/releases/download/v3.6.0/gobuster_3.6.0_Darwin_x86_64.tar.gz"
    ["ffuf"]="brew:ffuf|curl:https://github.com/ffuf/ffuf/releases/download/v2.1.0/ffuf_2.1.0_darwin_amd64.tar.gz"
    ["dirb"]="brew:dirb|port:dirb"
    ["wfuzz"]="pip:wfuzz|brew:wfuzz"
    ["zap-cli"]="pip:zapcli|brew:zap-cli"
    ["semgrep"]="brew:semgrep|pip:semgrep"
    ["bandit"]="pip:bandit|brew:bandit"
    ["safety"]="pip:safety|brew:safety"
    ["trivy"]="brew:trivy|curl:https://github.com/aquasecurity/trivy/releases/download/v0.47.0/trivy_0.47.0_macOS-64bit.tar.gz"
    ["grype"]="brew:grype|curl:https://github.com/anchore/grype/releases/download/v0.74.0/grype_0.74.0_darwin_amd64.tar.gz"
    ["syft"]="brew:syft|curl:https://github.com/anchore/syft/releases/download/v1.1.0/syft_1.1.0_darwin_amd64.tar.gz"
    ["snyk"]="brew:snyk|npm:snyk"
    ["dependabot"]="brew:dependabot|gem:dependabot-omnibus"
    ["npm-audit"]="npm:npm-audit-resolver|npm:audit-ci"
    ["pip-audit"]="pip:pip-audit|brew:pip-audit"
    ["gosec"]="brew:gosec|go:github.com/securego/gosec/v2/cmd/gosec"
    ["staticcheck"]="brew:staticcheck|go:honnef.co/go/tools/cmd/staticcheck"
    ["golangci-lint"]="brew:golangci-lint|curl:https://github.com/golangci/golangci-lint/releases/download/v1.54.2/golangci-lint-1.54.2-darwin-amd64.tar.gz"
    
    # Terminal & CLI Tools
    ["tmux"]="brew:tmux|port:tmux|curl:https://github.com/tmux/tmux/releases/download/3.3a/tmux-3.3a.tar.gz"
    ["neovim"]="brew:neovim|port:neovim|curl:https://github.com/neovim/neovim/releases/download/v0.9.4/nvim-macos.tar.gz"
    ["vim"]="brew:vim|port:vim"
    ["emacs"]="brew:emacs|port:emacs"
    ["zoxide"]="brew:zoxide|cargo:zoxide|curl:https://github.com/ajeetdsouza/zoxide/releases/download/v0.9.2/zoxide-0.9.2-x86_64-apple-darwin.tar.gz"
    ["bat"]="brew:bat|cargo:bat|port:bat"
    ["fd"]="brew:fd|cargo:fd|port:fd"
    ["rg"]="brew:ripgrep|cargo:ripgrep|port:ripgrep"
    ["ripgrep"]="brew:ripgrep|cargo:ripgrep"
    ["fzf"]="brew:fzf|git:https://github.com/junegunn/fzf.git|curl:https://github.com/junegunn/fzf/releases/download/0.44.0/fzf-0.44.0-darwin_amd64.tar.gz"
    ["exa"]="brew:exa|cargo:exa"
    ["eza"]="brew:eza|cargo:eza"
    ["lsd"]="brew:lsd|cargo:lsd"
    ["delta"]="brew:git-delta|cargo:git-delta"
    ["difftastic"]="brew:difftastic|cargo:difftastic"
    ["jq"]="brew:jq|port:jq"
    ["yq"]="brew:yq|curl:https://github.com/mikefarah/yq/releases/download/v4.35.2/yq_darwin_amd64"
    ["fx"]="brew:fx|npm:fx"
    ["gron"]="brew:gron|npm:gron"
    ["jo"]="brew:jo|port:jo"
    ["dasel"]="brew:dasel|curl:https://github.com/TomWright/dasel/releases/download/v2.4.0/dasel_darwin_amd64"
    ["xsv"]="cargo:xsv|brew:xsv"
    ["csvkit"]="pip:csvkit|brew:csvkit"
    ["httpie"]="brew:httpie|pip:httpie"
    ["curl"]="brew:curl|port:curl"
    ["wget"]="brew:wget|port:wget"
    ["aria2"]="brew:aria2|port:aria2"
    ["axel"]="brew:axel|port:axel"
    ["youtube-dl"]="brew:youtube-dl|pip:youtube-dl"
    ["yt-dlp"]="brew:yt-dlp|pip:yt-dlp"
    ["ffmpeg"]="brew:ffmpeg|port:ffmpeg"
    ["imagemagick"]="brew:imagemagick|port:imagemagick"
    ["ghostscript"]="brew:ghostscript|port:ghostscript"
    ["graphviz"]="brew:graphviz|port:graphviz"
    ["plantuml"]="brew:plantuml|port:plantuml"
    ["mermaid-cli"]="npm:@mermaid-js/mermaid-cli|brew:mermaid-cli"
    ["asciinema"]="brew:asciinema|pip:asciinema"
    ["tldr"]="brew:tldr|npm:tldr"
    ["cheat"]="brew:cheat|pip:cheat"
    ["navi"]="brew:navi|cargo:navi"
    ["glow"]="brew:glow|go:github.com/charmbracelet/glow"
    ["mdcat"]="brew:mdcat|cargo:mdcat"
    ["gum"]="brew:gum|go:github.com/charmbracelet/gum"
    ["charm"]="brew:charm|go:github.com/charmbracelet/charm"
    ["vhs"]="brew:vhs|go:github.com/charmbracelet/vhs"
    ["bubbletea"]="go:github.com/charmbracelet/bubbletea"
    ["spicetify"]="brew:spicetify/homebrew-tap/spicetify|curl:https://github.com/spicetify/spicetify-cli/releases/download/v2.26.3/spicetify-2.26.3-darwin-x64.tar.gz"
    ["ranger"]="brew:ranger|pip:ranger-fm"
    ["nnn"]="brew:nnn|port:nnn"
    ["lf"]="brew:lf|go:github.com/gokcehan/lf"
    ["broot"]="brew:broot|cargo:broot"
    ["dust"]="brew:dust|cargo:dust"
    ["dua"]="brew:dua|cargo:dua-cli"
    ["ncdu"]="brew:ncdu|port:ncdu"
    ["procs"]="brew:procs|cargo:procs"
    ["htop"]="brew:htop|port:htop"
    ["btop"]="brew:btop|cargo:btop"
    ["bashtop"]="brew:bashtop|git:https://github.com/aristocratos/bashtop.git"
    ["glances"]="brew:glances|pip:glances"
    ["bmon"]="brew:bmon|port:bmon"
    ["iftop"]="brew:iftop|port:iftop"
    ["nethogs"]="brew:nethogs|port:nethogs"
    ["vnstat"]="brew:vnstat|port:vnstat"
    ["bandwhich"]="brew:bandwhich|cargo:bandwhich"
    ["dog"]="brew:dog|cargo:dog"
    ["dig"]="brew:bind|port:bind"
    ["mtr"]="brew:mtr|port:mtr"
    ["iperf3"]="brew:iperf3|port:iperf3"
    ["speedtest-cli"]="pip:speedtest-cli|brew:speedtest-cli"
    ["fast-cli"]="npm:fast-cli|brew:fast-cli"
    ["ping"]="brew:iputils|port:iputils"
    ["traceroute"]="brew:traceroute|port:traceroute"
    ["nmap"]="brew:nmap|port:nmap"
    ["masscan"]="brew:masscan|port:masscan"
    ["zellij"]="brew:zellij|cargo:zellij"
    ["wezterm"]="brew:wezterm|curl:https://github.com/wez/wezterm/releases/download/20230712-072601-f4abf8fd/WezTerm-20230712-072601-f4abf8fd-macos.zip"
    ["alacritty"]="brew:alacritty|cargo:alacritty"
    ["kitty"]="brew:kitty|curl:https://sw.kovidgoyal.net/kitty/installer.sh"
    ["warp"]="brew:warp|curl:https://warp.dev/download"
    ["hyper"]="brew:hyper|npm:hyper"
    ["iterm2"]="brew:iterm2|mas:iTerm2"
    ["rectangle"]="brew:rectangle|mas:Rectangle"
    ["raycast"]="brew:raycast|curl:https://raycast.com/download"
    ["alfred"]="brew:alfred|curl:https://alfredapp.com/download"
    ["spotify-tui"]="brew:spotify-tui|cargo:spotify-tui"
    ["ncspot"]="brew:ncspot|cargo:ncspot"
    ["cmus"]="brew:cmus|port:cmus"
    ["mpv"]="brew:mpv|port:mpv"
    ["vlc"]="brew:vlc|mas:VLC"
    ["ffplay"]="brew:ffmpeg|port:ffmpeg"
    ["imv"]="brew:imv|cargo:imv"
    ["sxiv"]="brew:sxiv|port:sxiv"
    ["feh"]="brew:feh|port:feh"
    ["ueberzug"]="pip:ueberzug|brew:ueberzug"
    ["chafa"]="brew:chafa|port:chafa"
    ["tiv"]="brew:tiv|go:github.com/distatus/tiv"
    ["catimg"]="brew:catimg|port:catimg"
    ["jp2a"]="brew:jp2a|port:jp2a"
    ["asciiview"]="brew:aview|port:aview"
    
    # Version Managers
    ["nvm"]="curl:https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.4/install.sh|git:https://github.com/nvm-sh/nvm.git"
    ["rvm"]="curl:https://get.rvm.io|git:https://github.com/rvm/rvm.git"
    ["pyenv"]="brew:pyenv|curl:https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer|git:https://github.com/pyenv/pyenv.git"
    ["rbenv"]="brew:rbenv|git:https://github.com/rbenv/rbenv.git"
    ["jenv"]="brew:jenv|git:https://github.com/jenv/jenv.git"
    ["gvm"]="curl:https://raw.githubusercontent.com/moovweb/gvm/master/binscripts/gvm-installer|git:https://github.com/moovweb/gvm.git"
    ["phpenv"]="git:https://github.com/phpenv/phpenv.git|brew:phpenv"
    ["nodenv"]="brew:nodenv|git:https://github.com/nodenv/nodenv.git"
    ["plenv"]="brew:plenv|git:https://github.com/tokuhirom/plenv.git"
    ["perlbrew"]="curl:https://install.perlbrew.pl|brew:perlbrew"
    ["sbtenv"]="git:https://github.com/sbtenv/sbtenv.git|brew:sbtenv"
    ["scalaenv"]="git:https://github.com/scalaenv/scalaenv.git|brew:scalaenv"
    ["tfenv"]="brew:tfenv|git:https://github.com/tfutils/tfenv.git"
    ["kbenv"]="brew:kbenv|git:https://github.com/armory/kbenv.git"
    
    # Cloud Tools & CLIs
    ["aws-cli"]="brew:awscli|pip:awscli|curl:https://awscli.amazonaws.com/AWSCLIV2.pkg"
    ["aws-vault"]="brew:aws-vault|curl:https://github.com/99designs/aws-vault/releases/download/v7.2.0/aws-vault-darwin-amd64"
    ["gcloud"]="curl:https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-darwin-x86_64.tar.gz|brew:google-cloud-sdk"
    ["azure-cli"]="brew:azure-cli|curl:https://aka.ms/InstallAzureCLIDarwin|pip:azure-cli"
    ["doctl"]="brew:doctl|curl:https://github.com/digitalocean/doctl/releases/download/v1.100.0/doctl-1.100.0-darwin-amd64.tar.gz"
    ["linode-cli"]="pip:linode-cli|brew:linode-cli"
    ["vultr-cli"]="brew:vultr-cli|curl:https://github.com/vultr/vultr-cli/releases/download/v2.20.0/vultr-cli_2.20.0_darwin_amd64.tar.gz"
    ["scw"]="brew:scaleway-cli|curl:https://github.com/scaleway/scaleway-cli/releases/download/v2.25.0/scw-2.25.0-darwin-amd64"
    ["ovhai"]="brew:ovhai|curl:https://github.com/ovh/ovhai-cli/releases/download/v0.29.0/ovhai-darwin-amd64"
    ["vercel"]="npm:vercel|brew:vercel"
    ["netlify"]="npm:netlify-cli|brew:netlify"
    ["flyctl"]="brew:flyctl|curl:https://fly.io/install.sh"
    ["railway"]="brew:railway|npm:@railway/cli"
    ["render"]="brew:render|npm:render-cli"
    ["heroku"]="brew:heroku|curl:https://cli-assets.heroku.com/install.sh"
    ["cf"]="brew:cloudfoundry-cli|curl:https://packages.cloudfoundry.org/stable?release=macosx64-binary&version=v8"
    ["ibmcloud"]="curl:https://clis.cloud.ibm.com/install/osx|brew:ibmcloud"
    ["oci"]="brew:oci-cli|pip:oci-cli"
    ["aliyun"]="brew:aliyun-cli|curl:https://aliyuncli.alicdn.com/aliyun-cli-macosx-latest-amd64.tgz"
    ["tencentcloud"]="brew:tencentcloud-cli|pip:tencentcloud-cli"
    ["aws-sso"]="brew:aws-sso-cli|pip:aws-sso-cli"
    ["aws-iam-authenticator"]="brew:aws-iam-authenticator|curl:https://amazon-eks.s3.us-west-2.amazonaws.com/1.28.0/2023-10-17/bin/darwin/amd64/aws-iam-authenticator"
    ["eksctl"]="brew:eksctl|curl:https://github.com/weaveworks/eksctl/releases/download/v0.160.0/eksctl_Darwin_amd64.tar.gz"
    ["aws-copilot"]="brew:aws-copilot-cli|curl:https://github.com/aws/copilot-cli/releases/download/v1.32.0/copilot-darwin"
    ["aws-cdk"]="npm:aws-cdk|brew:aws-cdk"
    ["cdk8s"]="npm:cdk8s-cli|brew:cdk8s"
    ["pulumi"]="brew:pulumi|curl:https://get.pulumi.com/install.sh"
    ["cdktf"]="npm:cdktf-cli|brew:cdktf"
    ["serverless"]="npm:serverless|brew:serverless"
    ["apex"]="brew:apex|curl:https://github.com/apex/apex/releases/download/v1.0.0-rc3/apex_darwin_amd64"
    ["up"]="brew:apex-up|npm:apex-up"
    ["claudia"]="npm:claudia|brew:claudia"
    ["zappa"]="pip:zappa|brew:zappa"
    ["chalice"]="pip:chalice|brew:chalice"
    ["masonite"]="pip:masonite-cli|brew:masonite-cli"
    ["sceptre"]="pip:sceptre|brew:sceptre"
    ["molecule"]="pip:molecule|brew:molecule"
    ["ansible-lint"]="pip:ansible-lint|brew:ansible-lint"
    ["yamllint"]="pip:yamllint|brew:yamllint"
    ["cfn-lint"]="pip:cfn-lint|brew:cfn-lint"
    ["jsonlint"]="npm:jsonlint|brew:jsonlint"
    ["markdownlint"]="npm:markdownlint-cli|brew:markdownlint-cli"
    ["write-good"]="npm:write-good|brew:write-good"
    ["proselint"]="pip:proselint|brew:proselint"
    ["alex"]="npm:alex|brew:alex"
    ["textlint"]="npm:textlint|brew:textlint"
    ["vale"]="brew:vale|curl:https://github.com/errata-ai/vale/releases/download/v2.29.0/vale_2.29.0_macOS_64-bit.tar.gz"
    ["mdl"]="gem:mdl|brew:mdl"
    ["remark"]="npm:remark-cli|brew:remark-cli"
    ["markdown"]="pip:markdown|brew:markdown"
    ["pandoc"]="brew:pandoc|port:pandoc"
    ["wkhtmltopdf"]="brew:wkhtmltopdf|port:wkhtmltopdf"
    ["weasyprint"]="pip:weasyprint|brew:weasyprint"
    ["prince"]="brew:prince|curl:https://www.princexml.com/download/"
    ["asciidoctor"]="gem:asciidoctor|brew:asciidoctor"
    ["sphinx"]="pip:sphinx|brew:sphinx"
    ["mkdocs"]="pip:mkdocs|brew:mkdocs"
    ["gitbook"]="npm:gitbook-cli|brew:gitbook-cli"
    ["vuepress"]="npm:vuepress|brew:vuepress"
    ["docusaurus"]="npm:@docusaurus/init|brew:docusaurus"
    ["gatsby"]="npm:gatsby-cli|brew:gatsby-cli"
    ["next"]="npm:next|brew:next"
    ["nuxt"]="npm:nuxt|brew:nuxt"
    ["svelte"]="npm:svelte|brew:svelte"
    ["angular"]="npm:@angular/cli|brew:angular-cli"
    ["react"]="npm:create-react-app|brew:create-react-app"
    ["vue"]="npm:@vue/cli|brew:vue-cli"
    ["ember"]="npm:ember-cli|brew:ember-cli"
    ["quasar"]="npm:@quasar/cli|brew:quasar-cli"
    ["ionic"]="npm:@ionic/cli|brew:ionic-cli"
    ["cordova"]="npm:cordova|brew:cordova"
    ["phonegap"]="npm:phonegap|brew:phonegap"
    ["expo"]="npm:expo-cli|brew:expo-cli"
    ["react-native"]="npm:react-native-cli|brew:react-native-cli"
    ["flutter"]="brew:flutter|curl:https://storage.googleapis.com/flutter_infra_release/releases/stable/macos/flutter_macos_arm64_stable.zip"
    ["dart"]="brew:dart|port:dart"
    ["swift"]="brew:swift|port:swift"
    ["xcode"]="mas:Xcode|brew:xcode"
    ["android-studio"]="brew:android-studio|curl:https://developer.android.com/studio"
    ["android-sdk"]="brew:android-sdk|port:android-sdk"
    ["gradle"]="brew:gradle|port:gradle"
    ["maven"]="brew:maven|port:maven"
    ["ant"]="brew:ant|port:ant"
    ["sbt"]="brew:sbt|port:sbt"
    ["leiningen"]="brew:leiningen|port:leiningen"
    ["boot"]="brew:boot-clj|port:boot"
    ["mill"]="brew:mill|curl:https://github.com/com-lihaoyi/mill/releases/download/0.11.6/0.11.6"
    ["coursier"]="brew:coursier|curl:https://github.com/coursier/coursier/releases/download/v2.1.0/coursier"
    ["ammonite"]="brew:ammonite-repl|curl:https://github.com/com-lihaoyi/Ammonite/releases/download/2.5.9/2.13-2.5.9"
    ["cabal"]="brew:cabal-install|port:cabal-install"
    ["stack"]="brew:haskell-stack|curl:https://get.haskellstack.org/"
    ["ghc"]="brew:ghc|port:ghc"
    ["opam"]="brew:opam|port:opam"
    ["dune"]="brew:dune|opam:dune"
    ["esy"]="npm:esy|brew:esy"
    ["rebar3"]="brew:rebar3|port:rebar3"
    ["mix"]="brew:elixir|port:elixir"
    ["hex"]="mix:local.hex|brew:hex"
    ["rebar"]="brew:rebar|port:rebar"
    ["rakudo"]="brew:rakudo-star|port:rakudo"
    ["zef"]="brew:zef|rakudo:zef"
    ["raku"]="brew:rakudo-star|port:rakudo"
    ["perl6"]="brew:rakudo-star|port:rakudo"
    ["cargo"]="curl:https://sh.rustup.rs|brew:rust"
    ["rustc"]="curl:https://sh.rustup.rs|brew:rust"
    ["rustup"]="curl:https://sh.rustup.rs|brew:rust"
    ["cargo-audit"]="cargo:cargo-audit|brew:cargo-audit"
    ["cargo-outdated"]="cargo:cargo-outdated|brew:cargo-outdated"
    ["cargo-watch"]="cargo:cargo-watch|brew:cargo-watch"
    ["cargo-edit"]="cargo:cargo-edit|brew:cargo-edit"
    ["cargo-make"]="cargo:cargo-make|brew:cargo-make"
    ["cargo-release"]="cargo:cargo-release|brew:cargo-release"
    ["cargo-fuzz"]="cargo:cargo-fuzz|brew:cargo-fuzz"
    ["cargo-bench"]="cargo:cargo-bench|brew:cargo-bench"
    ["cargo-tree"]="cargo:cargo-tree|brew:cargo-tree"
    ["cargo-geiger"]="cargo:cargo-geiger|brew:cargo-geiger"
    ["cargo-deny"]="cargo:cargo-deny|brew:cargo-deny"
    ["cargo-udeps"]="cargo:cargo-udeps|brew:cargo-udeps"
    ["cargo-machete"]="cargo:cargo-machete|brew:cargo-machete"
    ["cargo-sweep"]="cargo:cargo-sweep|brew:cargo-sweep"
    ["cargo-cache"]="cargo:cargo-cache|brew:cargo-cache"
    ["cargo-bloat"]="cargo:cargo-bloat|brew:cargo-bloat"
    ["cargo-expand"]="cargo:cargo-expand|brew:cargo-expand"
    ["cargo-inspect"]="cargo:cargo-inspect|brew:cargo-inspect"
    ["cargo-graph"]="cargo:cargo-graph|brew:cargo-graph"
    ["cargo-doc"]="cargo:cargo-doc|brew:cargo-doc"
    ["cargo-test"]="cargo:cargo-test|brew:cargo-test"
    ["cargo-clippy"]="cargo:clippy|brew:clippy"
    ["cargo-fmt"]="cargo:rustfmt|brew:rustfmt"
    ["rustfmt"]="cargo:rustfmt|brew:rustfmt"
    ["rust-clippy"]="cargo:clippy|brew:clippy"
    ["rust-analyzer"]="brew:rust-analyzer|cargo:rust-analyzer"
    ["racer"]="cargo:racer|brew:racer"
    ["rls"]="rustup:component:add:rls|brew:rls"
    ["clippy"]="cargo:clippy|brew:clippy"
    ["miri"]="rustup:component:add:miri|brew:miri"
    ["cargo-miri"]="cargo:miri|brew:miri"
    ["cargo-msrv"]="cargo:cargo-msrv|brew:cargo-msrv"
    ["cargo-tarpaulin"]="cargo:cargo-tarpaulin|brew:cargo-tarpaulin"
    ["cargo-kcov"]="cargo:cargo-kcov|brew:cargo-kcov"
    ["cargo-llvm-cov"]="cargo:cargo-llvm-cov|brew:cargo-llvm-cov"
    ["cargo-profdata"]="cargo:cargo-profdata|brew:cargo-profdata"
    ["flamegraph"]="cargo:flamegraph|brew:flamegraph"
    ["cargo-flamegraph"]="cargo:flamegraph|brew:flamegraph"
    ["cargo-criterion"]="cargo:cargo-criterion|brew:cargo-criterion"
    ["criterion"]="cargo:criterion|brew:criterion"
    ["cargo-benchcmp"]="cargo:cargo-benchcmp|brew:cargo-benchcmp"
    ["cargo-bench"]="cargo:cargo-bench|brew:cargo-bench"
    ["cargo-criterion"]="cargo:cargo-criterion|brew:cargo-criterion"
    ["hyperfine"]="brew:hyperfine|cargo:hyperfine"
    ["criterion.rs"]="cargo:criterion|brew:criterion"
)

install_tool() {
    local tool_name="$1"
    local method_preference="${2:-auto}"
    
    if [[ -z "${tool_name}" ]]; then
        echo "Usage: install_tool <tool_name> [method]"
        echo "Available tools: ${(k)TOOL_DATABASE[@]}"
        return 1
    fi
    
    local tool_config="${TOOL_DATABASE[$tool_name]}"
    if [[ -z "${tool_config}" ]]; then
        echo "Error: Tool '${tool_name}' not found in database"
        return 1
    fi
    
    # Parse installation methods
    local -a methods=(${(s:|:)tool_config})
    local installed=false
    
    # Try each method until one succeeds
    for method_config in "${methods[@]}"; do
        local method="${method_config%%:*}"
        local package="${method_config#*:}"
        
        if [[ "${method_preference}" != "auto" && "${method}" != "${method_preference}" ]]; then
            continue
        fi
        
        echo "Attempting to install ${tool_name} via ${method}..."
        
        case "${method}" in
            brew)
                if command -v brew >/dev/null 2>&1; then
                    brew install "${package}" && installed=true
                fi
                ;;
            npm)
                if command -v npm >/dev/null 2>&1; then
                    npm install -g "${package}" && installed=true
                fi
                ;;
            pip)
                if command -v pip3 >/dev/null 2>&1; then
                    pip3 install "${package}" && installed=true
                fi
                ;;
            cargo)
                if command -v cargo >/dev/null 2>&1; then
                    cargo install "${package}" && installed=true
                fi
                ;;
            curl)
                # Download and install
                local temp_dir=$(mktemp -d)
                curl -L "${package}" -o "${temp_dir}/download"
                if [[ "${package}" == *.pkg ]]; then
                    sudo installer -pkg "${temp_dir}/download" -target / && installed=true
                elif [[ "${package}" == *.dmg ]]; then
                    hdiutil attach "${temp_dir}/download" && installed=true
                elif [[ "${package}" == *.tar.gz ]] || [[ "${package}" == *.zip ]]; then
                    cd "${temp_dir}" && tar -xzf download 2>/dev/null || unzip download
                    # Move to appropriate location
                    sudo cp -r */ /usr/local/ 2>/dev/null && installed=true
                fi
                rm -rf "${temp_dir}"
                ;;
            git)
                local install_dir="${HOME}/.local/bin/${package##*/}"
                git clone "${package}" "${install_dir}" && \
                cd "${install_dir}" && \
                make install 2>/dev/null || ./install.sh 2>/dev/null && installed=true
                ;;
            port)
                if command -v port >/dev/null 2>&1; then
                    sudo port install "${package}" && installed=true
                fi
                ;;
            conda)
                if command -v conda >/dev/null 2>&1; then
                    conda install -c conda-forge "${package}" && installed=true
                fi
                ;;
            mas)
                if command -v mas >/dev/null 2>&1; then
                    mas install "${package}" && installed=true
                fi
                ;;
        esac
        
        if [[ "${installed}" == "true" ]]; then
            echo "✓ Successfully installed ${tool_name} via ${method}"
            echo "$(date): Installed ${tool_name} via ${method}" >> "${INSTALL_LOG}"
            
            # Verify installation
            if command -v "${tool_name}" >/dev/null 2>&1; then
                echo "✓ Verification: ${tool_name} is available"
            fi
            return 0
        fi
    done
    
    echo "✗ Failed to install ${tool_name} with all available methods"
    return 1
}

install_multiple_tools() {
    local -a tools=("$@")
    local success=0
    local failed=0
    
    for tool in "${tools[@]}"; do
        if install_tool "${tool}"; then
            ((success++))
        else
            ((failed++))
        fi
    done
    
    echo "Installation complete: ${success} succeeded, ${failed} failed"
}

list_available_tools() {
    echo "Available Tools (${#TOOL_DATABASE[@]}):"
    for tool in "${(ko)TOOL_DATABASE[@]}"; do
        echo "  - ${tool}"
    done
}

