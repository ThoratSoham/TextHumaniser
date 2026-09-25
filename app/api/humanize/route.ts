import { NextResponse } from "next/server";
import { humanize } from "@/lib/pipeline";

export async function POST(request: Request) {
    try {
        const body = await request.json();
        const text = body.text;
        if (typeof text !== "string" || text.trim() === "") {
            return NextResponse.json(
                { error: "Please send some text."},
                { status: 400}
            );
        }
        const result = await humanize(text);
        return NextResponse.json({ result: result });
    } catch (error) {
        console.error(error);
        return NextResponse.json(
            { error: "Something went wrong. Is Ollama running?"},
            { status: 500 }
        );
    }
}