import datetime
import sys

import pefile

pe = pefile.PE(sys.argv[1])

print("[DOS 헤더]")
print("e_magic  :", hex(pe.DOS_HEADER.e_magic), "(MZ)")
print("e_lfanew :", hex(pe.DOS_HEADER.e_lfanew), "(NT 헤더 위치)")

nt = pe.NT_HEADERS
fh = pe.FILE_HEADER
oh = pe.OPTIONAL_HEADER
print("\n[NT 헤더]")
print("Signature      :", hex(nt.Signature), "(PE\\0\\0)")
print("Machine        :", hex(fh.Machine))
ts = datetime.datetime.fromtimestamp(fh.TimeDateStamp, datetime.timezone.utc)
print("컴파일 시각    :", ts.strftime("%Y-%m-%d %H:%M:%S"), "UTC")
print("구역 수        :", fh.NumberOfSections)
print("Subsystem      :", oh.Subsystem, pefile.SUBSYSTEM_TYPE.get(oh.Subsystem))
print("EntryPoint RVA :", hex(oh.AddressOfEntryPoint))
print("ImageBase      :", hex(oh.ImageBase))

print("\n[섹션]")
print(f"{'이름':8} {'가상크기':>9} {'원본크기':>9}  권한")
for s in pe.sections:
    ch = s.Characteristics
    perm = ("R" if ch & 0x40000000 else "-") + ("W" if ch & 0x80000000 else "-") + ("X" if ch & 0x20000000 else "-")
    name = s.Name.rstrip(b"\x00").decode()
    print(f"{name:8} {s.Misc_VirtualSize:>9} {s.SizeOfRawData:>9}  {perm}")

print("\n[임포트 표]")
for entry in pe.DIRECTORY_ENTRY_IMPORT:
    names = [i.name.decode() for i in entry.imports if i.name]
    print(entry.dll.decode(), f"({len(names)}개)")
    if "--all" in sys.argv:
        print("   ", ", ".join(names))
