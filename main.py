
from pathlib import Path
from extractor import extract_resume, extract_invoice


def main():

    print("\nAI RESUME AND INVOICE EXTRACTION")
    print("=" * 40)

    print("1. Resume Extraction")
    print("2. Invoice Extraction")

    choice = input("\nEnter your choice (1 or 2): ")

    print("\nPaste your document text below.")
    print("When finished, type END on a new line:")

    lines = []

    while True:
        line = input()

        if line.strip().upper() == "END":
            break

        lines.append(line)

    document_text = "\n".join(lines).strip()

    if not document_text:
        print("No document text provided.")
        return

    if choice == "1":
        result = extract_resume(document_text)
        print("\nRESUME EXTRACTION RESULT")

    elif choice == "2":
        result = extract_invoice(document_text)
        print("\nINVOICE EXTRACTION RESULT")

    else:
        print("Invalid choice!")
        return

    print("=" * 40)
    print(result.model_dump_json(indent=4))

    # Save extracted data
    output_folder = Path("output")
    output_folder.mkdir(exist_ok=True)

    filename = (
        "resume_extraction.json"
        if choice == "1"
        else "invoice_extraction.json"
    )

    output_path = output_folder / filename

    output_path.write_text(
        result.model_dump_json(indent=4),
        encoding="utf-8"
    )

    print(f"\nFile saved successfully: {output_path}")


if __name__ == "__main__":
    main()
