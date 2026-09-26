## 1.System Information
zhy@zhy-VMware-Virtual-Platform:~$ cat /etc/os-release
PRETTY_NAME="Ubuntu 24.04.5 LTS"
NAME="Ubuntu"
VERSION_ID="24.04"
VERSION="24.04.5 LTS (Noble Numbat)"
VERSION_CODENAME=noble
ID=ubuntu
ID_LIKE=debian
HOME_URL="https://www.ubuntu.com/"
SUPPORT_URL="https://help.ubuntu.com/"
BUG_REPORT_URL="https://bugs.launchpad.net/ubuntu/"
PRIVACY_POLICY_URL="https://www.ubuntu.com/legal/terms-and-policies/privacy-policy"
UBUNTU_CODENAME=noble
LOGO=ubuntu-logo
zhy@zhy-VMware-Virtual-Platform:~$ uname -r
7.0.0-34-generic
zhy@zhy-VMware-Virtual-Platform:~$ lscpu
架构：                       x86_64
  CPU 运行模式：             32-bit, 64-bit
  Address sizes:             45 bits physical, 48 bits virtual
  字节序：                   Little Endian
CPU:                         4
  在线 CPU 列表：            0-3
厂商 ID：                    GenuineIntel
  型号名称：                 Intel(R) Core(TM) i7-8565U CPU @ 1.80GHz
    CPU 系列：               6
    型号：                   142
    每个核的线程数：         1
    每个座的核数：           2
    座：                     2
    步进：                   12
    BogoMIPS：               3984.01
    标记：                   fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pg
                             e mca cmov pat pse36 clflush mmx fxsr sse sse2 ss h
                             t syscall nx pdpe1gb rdtscp lm constant_tsc arch_pe
                             rfmon nopl xtopology tsc_reliable nonstop_tsc cpuid
                              tsc_known_freq pni pclmulqdq ssse3 fma cx16 pcid s
                             se4_1 sse4_2 x2apic movbe popcnt aes xsave avx f16c
                              rdrand hypervisor lahf_lm abm 3dnowprefetch pti ss
                             bd ibrs ibpb stibp fsgsbase tsc_adjust bmi1 avx2 sm
                             ep bmi2 invpcid rdseed adx smap clflushopt xsaveopt
                              xsavec xgetbv1 xsaves arat md_clear flush_l1d arch
                             _capabilities
Virtualization features:     
  超管理器厂商：             VMware
  虚拟化类型：               完全
Caches (sum of all):         
  L1d:                       128 KiB (4 instances)
  L1i:                       128 KiB (4 instances)
  L2:                        1 MiB (4 instances)
  L3:                        16 MiB (2 instances)
NUMA:                        
  NUMA 节点：                1
  NUMA 节点0 CPU：           0-3
Vulnerabilities:             
  Gather data sampling:      Unknown: Dependent on hypervisor status
  Ghostwrite:                Not affected
  Indirect target selection: Mitigation; Aligned branch/return thunks
  Itlb multihit:             Not affected
  L1tf:                      Mitigation; PTE Inversion
  Mds:                       Mitigation; Clear CPU buffers; SMT Host state unkno
                             wn
  Meltdown:                  Mitigation; PTI
  Mmio stale data:           Mitigation; Clear CPU buffers; SMT Host state unkno
                             wn
  Old microcode:             Not affected
  Reg file data sampling:    Not affected
  Retbleed:                  Mitigation; IBRS
  Spec rstack overflow:      Not affected
  Spec store bypass:         Mitigation; Speculative Store Bypass disabled via p
                             rctl
  Spectre v1:                Mitigation; usercopy/swapgs barriers and __user poi
                             nter sanitization
  Spectre v2:                Mitigation; IBRS; IBPB conditional; STIBP disabled;
                              RSB filling; PBRSB-eIBRS Not affected; BHI SW loop
                             , KVM SW loop
  Srbds:                     Unknown: Dependent on hypervisor status
  Tsa:                       Not affected
  Tsx async abort:           Not affected
  Vmscape:                   Not affected
zhy@zhy-VMware-Virtual-Platform:~$ lspci | grep -Ei 'vga|3d|display'
00:0f.0 VGA compatible controller: VMware SVGA II Adapter
zhy@zhy-VMware-Virtual-Platform:~$ lspci -k | grep -EA3 'VGA|3D|Display'
00:0f.0 VGA compatible controller: VMware SVGA II Adapter
	Subsystem: VMware SVGA II Adapter
	Kernel driver in use: vmwgfx
	Kernel modules: vmwgfx
00:10.0 SCSI storage controller: Broadcom / LSI 53c1030 PCI-X Fusion-MPT Dual Ultra320 SCSI (rev 01)
zhy@zhy-VMware-Virtual-Platform:~$ lspci -k | grep -EA3 'VGA|3D|Display'
00:0f.0 VGA compatible controller: VMware SVGA II Adapter
	Subsystem: VMware SVGA II Adapter
	Kernel driver in use: vmwgfx
	Kernel modules: vmwgfx
00:10.0 SCSI storage controller: Broadcom / LSI 53c1030 PCI-X Fusion-MPT Dual Ultra320 SCSI (rev 01)
zhy@zhy-VMware-Virtual-Platform:~$ echo "$XDG_SESSION_TYPE"
wayland
zhy@zhy-VMware-Virtual-Platform:~$ echo "$DISPLAY"
:0
zhy@zhy-VMware-Virtual-Platform:~$ echo "$WAYLAND_DISPLAY"
wayland-0
zhy@zhy-VMware-Virtual-Platform:~$ nvidia-smi
找不到命令 “nvidia-smi”，但可以通过以下软件包安装它：
sudo apt install nvidia-utils-470-server  # version 470.256.02-0ubuntu0.24.04.1, or
sudo apt install nvidia-utils-535         # version 535.309.01-0ubuntu0.24.04.1
sudo apt install nvidia-utils-535-server  # version 535.309.01-0ubuntu0.24.04.1
sudo apt install nvidia-utils-565-server  # version 565.57.01-0ubuntu0.24.04.3
sudo apt install nvidia-utils-580         # version 580.159.03-0ubuntu0.24.04.1
sudo apt install nvidia-utils-580-server  # version 580.159.03-0ubuntu0.24.04.1
sudo apt install nvidia-utils-525         # version 525.147.05-0ubuntu1
sudo apt install nvidia-utils-525-server  # version 525.147.05-0ubuntu1
sudo apt install nvidia-utils-470         # version 470.256.02-0ubuntu0.24.04.1
sudo apt install nvidia-utils-550-server  # version 550.163.01-0ubuntu0.24.04.1
sudo apt install nvidia-utils-595         # version 595.71.05-0ubuntu0.24.04.1
sudo apt install nvidia-utils-595-server  # version 595.71.05-0ubuntu0.24.04.1
zhy@zhy-VMware-Virtual-Platform:~$ nvcc --version
找不到命令 “nvcc”，但可以通过以下软件包安装它：
sudo apt install nvidia-cuda-toolkit

## 2. Python Project A
