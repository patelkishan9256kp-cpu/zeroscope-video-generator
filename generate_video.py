import requests, sys, time

HF_API_URL = "https://api-inference.huggingface.co/models/cerspense/zeroscope_v2_576w"

def generate(prompt: str, token: str, output_file: str = "output.mp4", retries: int = 5):
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"inputs": prompt}
    for attempt in range(retries):
        try:
            print(f"Attempt {attempt+1}…")
            response = requests.post(HF_API_URL, headers=headers, json=payload)
            if response.status_code == 200:
                with open(output_file, "wb") as f:
                    f.write(response.content)
                print(f"Video saved to {output_file}")
                return
            else:
                # If we get a job ID, wait for the result
                job_id = response.json().get("id")
                if job_id:
                    print(f"Job started, waiting for {job_id}…")
                    time.sleep(30)
                    video_url = f"https://api-inference.huggingface.co/models/cerspense/zeroscope_v2_576w/{job_id}"
                    r = requests.get(video_url, headers=headers)
                    while r.status_code == 202:
                        time.sleep(10)
                        r = requests.get(video_url, headers=headers)
                    if r.status_code == 200:
                        with open(output_file, "wb") as f:
                            f.write(r.content)
                        print(f"Video saved to {output_file}")
                        return
        except Exception as e:
            print(f"Attempt {attempt+1} failed: {e}")
            time.sleep(10)
    print("Failed after all retries.")

if __name__ == "__main__":
    token = sys.argv[1]
    prompt = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) > 3 else "output.mp4"
    generate(prompt, token, output)
