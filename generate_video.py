import requests, sys, time

HF_API_URL = "https://api-inference.huggingface.co/models/cerspense/zeroscope_v2_576w"
headers = {"Authorization": f"Bearer {sys.argv[1]}"}   # Hugging Face token passed as first argument

def generate(prompt: str, output_file: str = "output.mp4"):
    payload = {"inputs": prompt}
    response = requests.post(HF_API_URL, headers=headers, json=payload)
    
    # The first response usually returns a job ID; the model runs asynchronously
    if response.status_code == 200:
        with open(output_file, "wb") as f:
            f.write(response.content)
        print(f"Video saved to {output_file}")
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
            else:
                print("Failed to fetch video after job completed")

if __name__ == "__main__":
    prompt = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) > 3 else "output.mp4"
    generate(prompt, output)
