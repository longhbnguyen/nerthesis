python run.py mono_en > mono_en_test.txt
python run.py mono_vn > mono_vn_test.txt
python run.py bi > bi_test.txt
python run.py mono_en mono_vn > mono_en_mono_vn_test.txt
python run.py mono_en bi > mono_en_bi_test.txt
python run.py mono_vn bi > mono_vn_bi_test.txt
python run.py mono_en mono_vn bi > mono_en_mono_vn_bi_test.txt
cp mono_en_test.txt mono_vn_test.txt bi_test.txt mono_en_mono_vn_test.txt mono_en_bi_test.txt mono_vn_bi_test.txt mono_en_mono_vn_bi_test.txt ./Result_Naive_NormalizeTranslationTransliteration/