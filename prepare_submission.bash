PREFIX=it3708_epuck_karlsen_vikjord_amundsen
CODE_TEMP_DIR=${PREFIX}_code

cd report && make && cd ..
cp report/report.pdf ${PREFIX}_report.pdf
cp -R swarm-epuck ${CODE_TEMP_DIR}
find ${CODE_TEMP_DIR} -name '*git*' | xargs rm -fr
find ${CODE_TEMP_DIR} -name '*wbproj*' | xargs rm -fr
zip -r ${PREFIX}_code.zip ${CODE_TEMP_DIR}
rm -fr ${CODE_TEMP_DIR}
