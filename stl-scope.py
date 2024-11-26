# ------------- IMPORTS ------------- #
import res


# ------------- GLOBALS ------------- #

gsi_readmap = [3,8,1,2,2,32,32,32,32,32,32,16,6,6,2,5,5,3,2,2,1,8,8,1,1,3,32,32,32,75,576]
tti_readmap = [1,2,1,1,4,4,1,1,1,112]

gsi_block = {
    "Code Page Number" : "",
    "Disk Format Code" : "",
    "Display Standard Code" : "",
    "Character Code Table" : "",
    "Language Code" : "",
    "Original Progamme Title" : "",
    "Original Episode Title" : "",
    "Translated Programme Title" : "",
    "Translated Episode Title" : "",
    "Translator's Name" : "",
    "Translator's Contact Details" : "",
    "Subtitle List Reference Code" : "",
    "Creation Date" : "",
    "Revision Date" : "",
    "Revision number" : "",
    "Total Number of TTI blocks" : "",
    "Total Number of subtitles" : "",
    "Total Number of subtitle groups" : "",
    "Max Characters in line" : "",
    "Max lines" : "",
    "TC Status" : "",
    "TC Start" : "",
    "TC First In-Cue" : "",
    "Total Number of Disks" : "",
    "Disk Number" : "",
    "Country of Origin" : "",
    "Publisher" : "",
    "Editor's Name" : "",
    "Editor's Contact Details" : "",
    "Spare Bytes" : "",
    "User Defined" : ""
    }


tti_block = {
    "Subtitle Group Number" : "",
    "Subtitle Number" : "",
    "Extension Block Number" : "",
    "Cumulative Status" : "",
    "Time Code In" : "",
    "Time Code Out" : "",
    "Vertical Position" : "",
    "Justification Code" : "",
    "Comment Flag" : "",
    "Text Field" : ""
}

tti_blocks = []

stlfile = "Testfile/test.stl"


# ------------- FUNCTIONS ------------- #

with open (stlfile, "rb") as file:
    codepage = "cp" + file.read(gsi_readmap[0]).decode("ascii")

with open (stlfile, "rb") as file:
    for byte, key in enumerate(gsi_block):
        val = file.read(gsi_readmap[byte]).decode(codepage)
        
        if val.isspace():
            val = "Undefined"

        val = val.strip()

        if key == "Code Page Number":
            val += " [" + res.struct_cpn[val] + "]"

        if key == "Disk Format Code":
            val += " [" + res.struct_dfc[val] + "]"

        if key == "Display Standard Code":
            if val != "Undefined":
                val += " " + res.struct_dsc[int(val)]

        if key == "Character Code Table":
            val += " [" + res.struct_cct[int(val)] + "]"

        if key == "Language Code":
            val += " [" + res.struct_lc[int(val, 16)] + "]"

        if key == "Creation Date" or key == "Revision Date":
            val += " [" + val[4:6] + "." + val[2:4] + "." + val[0:2] + "]"

        if key == "Revision number" or key == "Total Number of TTI blocks" or key == "Total Number of subtitles" or key == "Total Number of subtitle groups":
            val = str(int(val))
        
        if key == "Total Number of TTI blocks":
            val = int(val)

        if key == "TC Status":
            val += " [" + res.struct_tcs[int(val)] + "]"

        if key == "TC Start" or key == "TC First In-Cue":
            val = val[0:2] + ":" + val[2:4] + ":" + val[4:6] + ":" + val[6:8] 

        gsi_block[key] = val

    for key in gsi_block:
        print(key + " : " + str(gsi_block[key]))

    print("--------------------------------------------------")

    for tti in range(gsi_block["Total Number of TTI blocks"]):
        for byte, key in enumerate(tti_block):
            val = file.read(tti_readmap[byte]).hex()

            if key == "Subtitle Group Number":
                val = int(val, 16)

            if key == "Subtitle Number":
                val = str(int(val[2:4], 16) + int(val[0:2], 16) + 1)

            if key == "Extension Block Number":
                if val == "fe":
                    val += " [User Data]"
                if val == "ff":
                    val += " [None or End]"

            if key == "Cumulative Status":
                val += " [" + res.struct_cs[int(val)] + "]"

            if key == "Time Code In" or key == "Time Code Out":
                val = str(int(val[0:2], 16)).zfill(2) + ":" + str(int(val[2:4], 16)).zfill(2) + ":" + str(int(val[4:6], 16)).zfill(2) + ":" + str(int(val[6:8], 16)).zfill(2)

            if key == "Vertical Position":
                val = int(val, 16)

            if key == "Justification Code":
                val += " [" + res.struct_jc[int(val)] + "]"

            if key == "Comment Flag":
                val += " [" + res.struct_cf[int(val)] + "]"

            if key == "Text Field":
                val = val.upper()
                val_decoded = "\n--------------------------------------------------\n"
                for bytes in [val[i:i+2] for i in range (0, len(val), 2)]:
                    val_decoded += res.struct_iso_6937_2[bytes]
                    val = val_decoded

            tti_block[key] = val

        tti_blocks.append(tti_block.copy())

    for tti_block in tti_blocks:
        for key in tti_block:
            print (key + " : " + str(tti_block[key]))


