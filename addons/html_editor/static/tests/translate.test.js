import { expect, test } from "@odoo/hoot";
import { setupEditor } from "./_helpers/editor";
import { expandToolbar } from "./_helpers/toolbar";
import { TranslatePlugin } from "@html_editor/main/translate/translate_plugin";

// Vender intentionally does not expose Odoo-hosted paid AI/translation services.
// Keep a focused regression check instead of retaining tests that expect them.
test("Odoo-hosted paid translation controls are not available", async () => {
    await setupEditor("<p>te[s]t</p>", {
        config: { includePlugins: [TranslatePlugin] },
    });
    await expandToolbar();
    expect(".o-we-toolbar .btn[name='translate']").toHaveCount(0);
});
