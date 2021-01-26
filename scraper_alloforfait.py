import requests
import re
import unidecode


class Package:
    """Class showing channel packages"""
    
    def __init__(self, package):
        self.package = package

    def channels(self):

        response = requests.get("https://alloforfait.fr/tv/"+self.package+"/")

        if response.status_code == 200:

            channels = []
            if self.package == "free":
                selected = re.findall("<td>[0-9]*</td>\n<td>.*\n<td>Freebox TV</td>", response.text)
                for channel in selected:
                    channel = unidecode.unidecode(channel[4:-25]).upper()
                    index = channel.find("</TD>\n<TD>")
                    channels.append((int(channel[:index]), channel[index+10:]))
                channels = channels[1:]
                channels.sort()

            elif self.package == "sfr":
                selected_hd = re.findall("<td>[0-9]*</td>\n<td>.*</td>\n<td>HD</td>", response.text)
                for channel in selected_hd:
                    channel = unidecode.unidecode(channel[4:-17]).upper()
                    index = channel.find("</TD>\n<TD>")
                    channels.append((int(channel[:index]), channel[index+10:]))
                selected = re.findall("<td>[0-9]*</td>\n<td>.*</td>\n<td></td>", response.text)
                for channel in selected:
                    channel = unidecode.unidecode(channel[4:-15]).upper()
                    index = channel.find("</TD>\n<TD>")
                    channels.append((int(channel[:index]), channel[index+10:]))
                channels.sort()

            elif self.package == "bbox-bouygues-telecom":
                selected = re.findall("<tr>\n<td>[0-9]*</td>\n<td>.*</td>\n</tr>", response.text)
                for channel in selected[1:]:
                    channel = unidecode.unidecode(channel[9:-11]).upper()
                    index = channel.find("</TD>\n<TD>")
                    channels.append((int(channel[:index]), channel[index+10:]))
                channels.sort()
        else:
            channels = []

        al_jazeera = True
        n = 0
        for channel in channels:
            if channel[1].find("&AMP;") != -1:
                name = channel[1]
                channels[n] = (channel[0], name.replace("&AMP;", "&"))
            elif channel[1].find("&RSQUO;") != -1:
                name = channel[1]
                channels[n] = (channel[0], name.replace("&RSQUO;", "'"))
            elif channel[1][:3] == "LCP":
                channels[n] = (channel[0], "LA CHAINE PARLEMENTAIRE")
            elif channel[1][:9] == "BLOOMBERG":
                channels[n] = (channel[0], "BLOOMBERG UK-EUROPE")
            elif channel[1][:18] == "AL JAZEERA ANGLAIS" or channel[1] == "AL JAZEERA":
                if al_jazeera:
                    channels[n] = (channel[0], "AL JAZEERA ENGLISH")
                al_jazeera = False
            elif channel[1] == "TV5" or channel[1] == "TV5 MONDE":
                channels[n] = (channel[0], "TV5MONDE")
            elif channel[1] == "CANAL + (EN CLAIR)" or channel[1] == "CANAL+ (EN CLAIR)":
                channels[n] = (channel[0], "CANAL+")
            elif channel[1] == "BBC WORLD":
                channels[n] = (channel[0], "BBC WORLD NEWS")
            elif channel[1] == "TELE NANTES":
                channels[n] = (channel[0], "TELENANTES")

            n+=1

        return channels
