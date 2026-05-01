
SCORE := undead_siege.mscz
META := undead_siege.meta
PDF := undead_siege.pdf
RAW := undead_siege_1_raw.flac
COMP:= undead_siege_2_comp.flac
NORM:= undead_siege_3_norm.flac
OGG := undead_siege.ogg
MEAS_JSON := loudness_norm.json

default:
	@echo "make export 	- Exports score PDF and audio flac using MuseScore"
	@echo "make convert - Adjusts exported track's loudness and outputs ogg file"

export:
	@echo "Exporting the score to pdf..."
	mscore -o $(PDF) $(SCORE)
	@echo "Exporting MuseScore project to flac..."
	mscore -o $(RAW) $(SCORE)

convert:	
	@echo "Applying mild audio compression.."
	ffmpeg -y -i $(RAW) -af "compand=points=-80/-80|-6/-6|0/-3.8|20/3.5" $(COMP)
	@echo "Generating a loudnorm measurement file.."
	ffmpeg -y -i $(COMP) -af "loudnorm=tp=0.0:print_format=json" -f null - 2> "$(MEAS_JSON)"
	@echo "Pass 2: applying volume adjustment based on input_tp.."
	TPV=$$(sed -n 's/.*"input_tp"[[:space:]]*:[[:space:]]*"-\([^"]*\)".*/\1/p' $(MEAS_JSON)); \
	ffmpeg -y -i $(COMP) -af "volume=volume=$$TPV""dB" $(NORM)
	@echo "Exporting ogg file.."
	ffmpeg -y -i $(NORM) -i $(META) -map_metadata 1 \
	-ar 44100 -codec:a libvorbis -qscale:a 10 $(OGG)
