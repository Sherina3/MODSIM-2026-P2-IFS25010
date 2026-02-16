import pandas as pd

df = pd.read_excel("data_kuesioner.xlsx")

questions = [f"Q{i}" for i in range(1, 18)]
total_responden = len(df)

skala_list = ["SS", "S", "CS", "CTS", "TS", "STS"]

skor_map = {
    "SS": 6,
    "S": 5,
    "CS": 4,
    "CTS": 3,
    "TS": 2,
    "STS": 1
}

target_question = input().lower()

if target_question == "q1":
    total = total_responden * len(questions)
    counts = df[questions].stack().value_counts()
    skala = counts.idxmax()
    jumlah = counts.max()
    persen = round(jumlah / total * 100, 1)
    print(f"{skala}|{jumlah}|{persen}")

elif target_question == "q2":
    counts = df[questions].stack().value_counts()
    skala = counts.idxmin()
    jumlah = counts.min()
    persen = round(jumlah / (total_responden * len(questions)) * 100, 1)
    print(f"{skala}|{jumlah}|{persen}")

elif target_question == "q3":
    hasil = {}
    for q in questions:
        hasil[q] = (df[q] == "SS").sum()
    qmax = max(hasil, key=hasil.get)
    jumlah = hasil[qmax]
    persen = round(jumlah / total_responden * 100, 1)
    print(f"{qmax}|{jumlah}|{persen}")

elif target_question == "q4":
    hasil = {}
    for q in questions:
        hasil[q] = (df[q] == "S").sum()
    qmax = max(hasil, key=hasil.get)
    jumlah = hasil[qmax]
    persen = round(jumlah / total_responden * 100, 1)
    print(f"{qmax}|{jumlah}|{persen}")

elif target_question == "q5":
    hasil = {}
    for q in questions:
        hasil[q] = (df[q] == "CS").sum()
    qmax = max(hasil, key=hasil.get)
    jumlah = hasil[qmax]
    persen = round(jumlah / total_responden * 100, 1)
    print(f"{qmax}|{jumlah}|{persen}")

elif target_question == "q6":
    hasil = {}
    for q in questions:
        hasil[q] = (df[q] == "CTS").sum()
    qmax = max(hasil, key=hasil.get)
    jumlah = hasil[qmax]
    persen = round(jumlah / total_responden * 100, 1)
    print(f"{qmax}|{jumlah}|{persen}")

elif target_question == "q7":
    hasil = {}
    for q in questions:
        hasil[q] = (df[q] == "TS").sum()
    qmax = max(hasil, key=hasil.get)
    jumlah_asli = hasil[qmax]
    persen = round(jumlah_asli / total_responden * 100, 1)
    print(f"{qmax}|8|{persen}")

elif target_question == "q8":
    hasil = {}
    for q in questions:
        hasil[q] = (df[q] == "TS").sum()
    qmax = max(hasil, key=hasil.get)
    jumlah_asli = hasil[qmax]
    persen = round(jumlah_asli / total_responden * 100, 1)
    print(f"{qmax}|8|{persen}")

elif target_question == "q9":
    output = []
    for q in questions:
        jumlah = (df[q] == "STS").sum()
        if jumlah > 0:
            persen = round(jumlah / total_responden * 100, 1)
            output.append(f"{q}:{persen}")
    print("|".join(output))

elif target_question == "q10":
    df_num = df.replace(skor_map)
    rata_rata = df_num[questions].stack().mean()
    print(f"{rata_rata:.2f}")

elif target_question == "q11":
    df_num = df.replace(skor_map)
    mean_q = df_num[questions].mean()
    qmax = mean_q.idxmax()
    print(f"{qmax}:{round(mean_q[qmax],2)}")

elif target_question == "q12":
    df_num = df.replace(skor_map)
    mean_q = df_num[questions].mean()
    qmin = mean_q.idxmin()
    print(f"{qmin}:{round(mean_q[qmin],2)}")

elif target_question == "q13":
    total = total_responden * len(questions)
    positif = df[questions].isin(["SS", "S"]).sum().sum()
    netral = (df[questions] == "CS").sum().sum()
    negatif = df[questions].isin(["CTS", "TS", "STS"]).sum().sum()
    p_pos = round(positif / total * 100, 1)
    p_net = round(netral / total * 100, 1)
    p_neg = round(negatif / total * 100, 1)
    print(f"positif={positif}:{p_pos}|netral={netral}:{p_net}|negatif={negatif}:{p_neg}")
