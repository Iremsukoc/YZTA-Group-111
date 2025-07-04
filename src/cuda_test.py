import torch
print("CUDA kullanılıyor mu?", torch.cuda.is_available())
print("GPU:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "Yok")
