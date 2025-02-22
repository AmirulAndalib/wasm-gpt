# WasmGPT

ChatGPT-like chatbot in the browser using ggml and emscripten. No API keys required. No server required. No data is sent to any server.

This demo uses a [Cerebras-GPT-1.3B-Alpaca-SP](https://huggingface.co/lxe/Cerebras-GPT-1.3B-Alpaca-SP), which is a version of the [Cerebras-GPT-1.3B](https://huggingface.co/cerebras/Cerebras-GPT-1.3B) model LoRA-finetuned on the [Alpaca](https://huggingface.co/datasets/tatsu-lab/alpaca) dataset. 

- [Demo](https://lxe.co/wasmgpt/)

### Limitations

 - The model is very hallucinatory and can generate very incorrect text. 
 - I limited initial system prompt and removed memory/context for speed.
 - The model is around 900MB and takes a while to load. 
 - Doesn't work on mobile safari. Probably won't work in all browsers.
 - ggml's implementation of gpt2 doesn't have repetition penalty (TODO), making it very repetitive
 
### TODOs

 - [ ] Less unhinged model support
 - [X] Repetition penalty
 - [ ] Longer context

### How to run locally

1. Have emscripten installed and activated

2. Clone this repo:

```
git clone -b wasm-demo https://github.com/lxe/ggml.git
cd ggml
```

2. In order to make wasm work, you need to serve it over https and provide Cross-Origin-Embedder-Policy and Cross-Origin-Opener-Policy headers. You can use the following commands to generate a self-signed certificate.

```
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes \
-subj "/CN=localhost" -addext "subjectAltName = DNS:localhost"
```

You will also need to add the certificate to your browser's root store.

3. Build the software and run the server:

```
mkdir build
cd build
emcmake cmake ..
make gpt-2
cd .. && python server.py
```

###

# ggml

Tensor library for machine learning

***Note that this project is under development and not ready for production use. \
Some of the development is currently happening in the [llama.cpp](https://github.com/ggerganov/llama.cpp) and [whisper.cpp](https://github.com/ggerganov/whisper.cpp) repos***

## Features

- Written in C
- 16-bit float support
- 4-bit integer quantization support
- Automatic differentiation (WIP in progress)
- ADAM and L-BFGS optimizers
- Optimized for Apple silicon via NEON intrinsics and Accelerate framework
- On x86 architectures utilzes AVX intrinsics
- No third-party dependencies
- Zero memory allocations during runtime

## Roadmap

- [X] Example of GPT-2 inference [examples/gpt-2](https://github.com/ggerganov/ggml/tree/master/examples/gpt-2)
- [X] Example of GPT-J inference [examples/gpt-j](https://github.com/ggerganov/ggml/tree/master/examples/gpt-j)
- [X] Example of Whisper inference [examples/whisper](https://github.com/ggerganov/ggml/tree/master/examples/whisper)
- [X] Support 4-bit integer quantization https://github.com/ggerganov/ggml/pull/27
- [X] Example of Cerebras-GPT inference [examples/gpt-2](https://github.com/ggerganov/ggml/tree/master/examples/gpt-2)
- [ ] Example of FLAN-T5 inference https://github.com/ggerganov/ggml/pull/12
- [X] Example of LLaMA inference [ggerganov/llama.cpp](https://github.com/ggerganov/llama.cpp)
- [X] Example of RWKV inference [saharNooby/rwkv.cpp](https://github.com/saharNooby/rwkv.cpp)
- [ ] Example of [SAM](https://github.com/facebookresearch/segment-anything) inference
- [ ] Idea for GPU support: https://github.com/ggerganov/llama.cpp/discussions/915
- [X] Example of StableLM (GPT-NeoX) inference [examples/stablelm](https://github.com/ggerganov/ggml/tree/master/examples/stablelm)

## Whisper inference (example)

With ggml you can efficiently run [Whisper](examples/whisper) inference on the CPU.

Memory requirements:

| Model  | Disk   | Mem     |
| ---    | ---    | ---     |
| tiny   |  75 MB | ~280 MB |
| base   | 142 MB | ~430 MB |
| small  | 466 MB | ~1.0 GB |
| medium | 1.5 GB | ~2.6 GB |
| large  | 2.9 GB | ~4.7 GB |

## GPT inference (example)

With ggml you can efficiently run [GPT-2](examples/gpt-2) and [GPT-J](examples/gpt-j) inference on the CPU.

Here is how to run the example programs:

```bash
# Build ggml + examples
git clone https://github.com/ggerganov/ggml
cd ggml
mkdir build && cd build
cmake ..
make -j4 gpt-2 gpt-j

# Run the GPT-2 small 117M model
../examples/gpt-2/download-ggml-model.sh 117M
./bin/gpt-2 -m models/gpt-2-117M/ggml-model.bin -p "This is an example"

# Run the GPT-J 6B model (requires 12GB disk space and 16GB CPU RAM)
../examples/gpt-j/download-ggml-model.sh 6B
./bin/gpt-j -m models/gpt-j-6B/ggml-model.bin -p "This is an example"

# Run the Cerebras-GPT 111M model
# Download from: https://huggingface.co/cerebras
python3 ../examples/gpt-2/convert-cerebras-to-ggml.py /path/to/Cerebras-GPT-111M/
./bin/gpt-2 -m /path/to/Cerebras-GPT-111M/ggml-model-f16.bin -p "This is an example"
```

The inference speeds that I get for the different models on my 32GB MacBook M1 Pro are as follows:

| Model | Size  | Time / Token |
| ---   | ---   | ---    |
| GPT-2 |  117M |   5 ms |
| GPT-2 |  345M |  12 ms |
| GPT-2 |  774M |  23 ms |
| GPT-2 | 1558M |  42 ms |
| ---   | ---   | ---    |
| GPT-J |    6B | 125 ms |

For more information, checkout the corresponding programs in the [examples](examples) folder.
