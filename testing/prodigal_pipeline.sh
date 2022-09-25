#!/bin/bash
# NC_015733
# this list of ids should work for every soil reference genome
ids=(NC_010572.1 NC_015635.1 NC_013132.1 NC_014618.1 NC_009342.1 NC_010163.1 NC_009712.1 NC_011772.1 NC_012918.1 NC_013173.1 NC_004343.2 NC_014659.1 NC_008380.1 NC_011725.1 NC_011660.1 NC_009483.1 NC_007492.2 NC_013061.1 NC_012522.1 NC_012488.1 NC_008343.1 NC_007798.1 NC_007777.1 NC_008314.1 NC_009505.1 NC_007624.1 NC_007761.1 NC_013722.1 NC_012563.1 NC_010677.1 NC_008752.1 NC_011898.1 NC_004663.1 NC_008705.1 NC_015567.1 NC_015137.1 NC_014614.1 NC_010084.1 NC_012778.1 NC_008699.1 NC_014655.1 NC_013743.1 NC_002936.3 NC_003062.2 NC_008508.1 NC_011729.1 NC_013016.1 NC_013850.1 NC_006351.1 NC_006582.1 NC_003295.1 NC_009698.1 NC_014100.1 NC_004572.3 NC_010682.1 NC_007517.1 NC_007794.1 NC_014507.1 NC_011969.1 NC_010694.1 NC_008027.1 NC_011894.1 NC_010505.1 NC_014815.1 NC_015707.1 NC_014117.1 NC_009725.1 NC_014394.1 NC_005773.3 NC_003902.1 NC_010338.1 NC_010337.2 NC_010103.1 NC_014639.1 NC_014013.1 NC_002578.1 NC_013943.1 .DS_Store NC_004551.1 NC_010512.1 NC_014551.1 NC_015593.1 NC_014228.1 NC_007404.1 NC_006350.1 NC_008509.1 NC_007613.1 NC_011662.2 NC_002937.3 NC_009524.1 NC_003063.2 NC_012850.1 NC_015696.1 NC_007644.1 NC_014654.1 NC_013892.1 NC_010617.1 NC_009436.1 NC_010528.1 NC_011769.1 NC_009565.1 NC_012796.1 NC_014479.1 NC_012721.2 NC_009050.1 NC_015589.1 NC_009953.1 NC_015136.1 NC_010508.1 NC_010676.1 NC_015474.1 NC_015161.1 NC_009142.1 NC_009512.1 NC_007760.1 NC_009441.1 NC_011071.1 NC_014623.1 NC_011837.1 NC_010725.1 NC_009504.1 NC_002939.5 NC_015177.1 NC_009338.1 NC_005966.1 NC_010322.1 NC_005823.1 NC_009380.1 NC_012489.1 NC_007493.2 NC_008786.1 NC_014483.2 NC_004463.1 NC_004342.2 NC_014658.1 NC_010162.1 NC_011773.1 NC_015675.1 NC_002516.2 NC_008544.1 NC_010524.1 NC_014834.1 NC_015726.1 NC_015376.1 NC_006274.1 NC_006624.1 NC_009617.1 NC_015634.1 NC_014307.1 NC_004757.1 NC_008261.1 NC_008148.1 NC_011369.1 NC_002971.3 NC_007086.1 NC_014215.1 NC_013929.1 NC_012791.1 NC_009077.1 NC_015687.1 NC_014829.1 NC_010169.1 NC_012857.1 NC_007356.1 NC_014311.1 NC_007498.2 NC_004129.6 NC_005296.1 NC_010581.1 NC_007614.1 NC_015594.1 NC_011884.1 NC_013766.2 NC_004556.1 NC_010515.1 NC_015717.1 NC_007907.1 NC_011979.1 NC_013552.1 NC_007511.1 NC_003552.1 NC_014151.1 NC_014501.1 NC_002570.2 NC_011083.1 NC_014002.1 NC_010104.1 NC_010554.1 NC_014844.1 NC_014393.1 NC_009667.1 NC_011365.1 NC_013421.1 NC_012660.1 NC_014833.1 NC_008543.1 NC_014976.1 NC_006361.1 NC_008390.1 NC_007435.1 NC_015222.1 NC_013525.1 NC_003030.1 NC_014171.1 NC_007618.1 NC_014034.1 NC_011666.1 NC_009256.1 NC_007494.2 NC_008781.1 NC_006834.1 NC_013159.1 NC_005824.1 NC_015577.1 NC_015520.1 NC_011830.1 NC_010688.1 NC_011963.1 NC_014632.1 NC_013118.1 NC_009515.1 NC_009664.2 NC_008095.1 NC_015425.1 NC_008702.1 NC_013119.1 NC_009848.2 NC_015167.1 NC_006177.1 NC_009328.1 NC_014625.1 NC_014330.1 NC_008313.1 NC_014019.1 NC_015433.1 NC_009943.1 NC_009484.1 NC_011958.1 NC_002678.2 NC_014259.1 NC_003155.4 NC_011149.1 NC_009715.1 NC_014961.1 NC_013861.1 NC_008391.1 NC_007434.1 NC_010172.1 NC_008542.1 NC_014166.1 NC_000963.1 NC_007947.1 NC_013512.1 NC_010943.1 NC_012971.2 NC_013729.1 NC_014500.1 NC_012207.1 NC_011094.1 NC_007510.1 NC_010001.1 NC_013768.1 NC_007681.1 NC_004557.1 NC_012483.1 NC_006511.1 NC_004193.1 NC_015151.1 NC_007880.1 NC_015690.1 NC_010168.1 NC_012856.1 NC_011145.1 NC_003361.3 NC_003197.1 NC_007204.1 NC_009076.1 NC_008149.1 NC_013355.1 NC_002927.3 NC_009720.1 NC_010501.1 NC_015216.1 NC_015580.1 NC_010628.1 NC_010556.1 NC_008536.1 NC_014145.1 NC_014000.1 NC_014153.1 NC_015312.1 NC_012438.1 NC_008609.1 NC_010002.1 NC_013854.1 NC_015596.1 NC_010794.1 NC_011886.1 NC_012947.1 NC_010995.1 NC_009464.1 NC_014313.1 NC_007530.2 NC_010184.1 NC_013194.1 NC_011146.1 NC_010468.1 NC_009075.1 NC_014217.1 NC_012724.2 NC_015847.1 NC_014722.1 NC_015563.1 NC_004722.1 NC_007948.1 NC_013791.2 NC_014958.1 NC_007509.1 NC_015758.1 NC_006932.1 NC_008740.1 NC_011832.1 NC_012658.1 NC_008255.1 NC_012988.1 NC_012967.1 NC_005125.1 NC_014734.1 NC_014364.1 NC_012526.1 NC_003272.1 NC_007925.1 NC_006322.1 NC_002944.2 NC_009254.1 NC_013209.1 NC_008150.1 NC_004347.2 NC_001263.1 NC_010167.1 NC_008392.1 NC_007964.1 NC_013161.1 NC_008541.1 NC_015723.1 NC_014831.1 NC_008146.1 NC_010577.1 NC_013971.1 NC_012726.1 NC_010465.1 NC_011761.1 NC_010520.1 NC_010170.1 NC_009078.1 NC_009428.1 NC_013530.1 NC_014963.1 NC_010473.1 NC_015734.1 NC_014125.1 NC_007973.1 NC_013526.1 NC_010424.1 NC_009255.1 NC_008278.1 NC_008782.1 NC_013967.1 NC_008595.1 NC_014365.1 NC_015061.1 NC_012659.1 NC_009445.1 NC_008254.1 NC_006933.1 NC_007508.1 NC_004631.1 NC_009668.1 NC_008700.1 NC_002973.6 NC_014666.1 NC_015145.1 NC_015846.1 NC_003212.1 NC_014538.1 NC_006155.1 NC_009074.1 NC_012792.1 NC_009832.1 NC_011852.1 NC_012004.1 NC_009648.1 NC_015684.1 NC_007355.1 NC_013592.1 NC_006905.1 NC_006513.1 NC_012803.1 NC_010994.1 NC_015578.1 NC_004369.1 NC_010516.1 NC_008825.1 NC_010845.1 NC_011757.1 NC_007512.1 NC_013947.1 NC_014328.1 NC_011080.1 NC_011983.1 NC_010557.1 NC_013510.1 NC_011891.1 NC_012881.1 NC_015565.1 NC_010622.1 NC_014118.1 NC_004547.2 NC_003997.3 NC_011988.1 NC_005861.1 NC_009511.1 NC_010730.1 NC_008245.1 NC_007333.1 NC_011658.1 NC_009792.1 NC_005877.1 NC_007519.1 NC_009012.1 NC_007775.1 NC_003366.1 NC_008711.1 NC_010321.1 NC_015573.1 NC_007958.1 NC_010634.1 NC_014319.1 NC_009439.1 NC_015676.1 NC_011770.1 NC_005363.1 NC_015733.1 NC_013921.1 NC_014972.1 NC_009706.1 NC_008639.1 NC_000913.3 NC_008510.1 NC_014817.1 NC_000964.3 NC_003901.1 NC_014006.1 NC_012214.1 NC_008463.1 NC_015601.1 NC_011992.1 NC_010842.1 NC_010511.1 NC_012039.1 NC_009675.1 NC_015656.1 NC_005085.1 NC_009049.1 NC_015590.1 NC_013595.1 NC_008789.1 NC_002488.3 NC_009659.1 NC_005945.1 NC_013891.1 NC_007651.1 NC_015379.1 NC_015683.1 NC_014211.1 NC_010602.1 NC_006369.1 NC_008009.1 NC_010086.1 NC_009494.2 NC_012669.1 NC_002689.2 NC_010087.1 NC_014210.1 NC_014640.1 NC_006368.1 NC_007650.1 NC_013890.1 NC_009434.1 NC_011004.1 NC_012917.1 NC_015381.1 NC_014314.1 NC_007168.1 NC_015856.1 NC_013202.1 NC_007406.1 NC_015591.1 NC_010843.1 NC_014103.1 NC_009674.1 NC_008435.1 NC_007514.1 NC_010681.1 NC_013941.1 NC_014622.2 NC_015315.1 NC_007778.1 NC_010814.1 NC_011985.1 NC_010678.1 NC_010551.1 NC_011205.1 NC_014816.1 NC_012491.1 NC_014924.1 NC_008511.1 NC_014532.1 NC_010571.1 NC_008268.1 NC_013131.1 NC_014973.1 NC_007963.1 NC_012632.1 NC_009654.1 NC_015677.1 NC_001264.1 NC_006958.1 NC_010530.1 NC_009438.1 NC_011726.1 NC_012673.1 NC_013961.1 NC_013062.1 NC_007164.1 NC_009480.1 NC_006831.1 NC_008593.1 NC_009802.1 NC_014733.1 NC_008710.1 NC_010320.1 NC_013446.2 NC_014158.1 NC_003909.8 NC_015460.1 NC_012560.1 NC_008497.1 NC_007298.1 NC_011989.1 NC_009455.1 NC_014119.1 NC_012472.1 NC_010336.1 NC_010623.1)
# ids=(NC_010572 NC_015635 NC_013132 NC_014618)

# ids=(NC_000913)
echo ${ids[@]}
for id in "${ids[@]}"
do
    echo $id
    # fetch_commmand="$(efetch -db nuccore -id $id -format fasta)"
    # echo $fetch_command >> data/input/$id.fasta

    mkdir data/output/prodigal/$id
    # prodigal_command="$(prodigal -i data/input/$id.fasta -o data/output/$id/$id.coords.gbk -d data/output/$id/$id.mrna.faa -a data/output/$id/$id.protein.faa)"
    strace -o data/output/prodigal/$id/$id.strace.txt -c -tt prodigal -i data/input/$id.fasta -o data/output/prodigal/$id/$id.coords.gbk -d data/output/prodigal/$id/$id.mrna.faa -a data/output/prodigal/$id/$id.protein.faa
    # prodigal -i data/input/$id.fasta -o data/output/prodigal/$id/$id.coords.gbk -d data/output/prodigal/$id/$id.mrna.faa -a data/output/prodigal/$id/$id.protein.faa
    # python script to compare the sequences.
done
# THis needs to recursively loop
# Can use trace to track how long the processes take
# ben@ben-amd:~/research/biol3209/prodigal_testing$ strace -o trace -c -Ttt ./pipeline.sh
