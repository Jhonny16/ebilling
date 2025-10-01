/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

import { SelectionField, selectionField } from "@web/views/fields/selection/selection_field";

import { Component } from "@odoo/owl";

export class DocumentStatePopover extends Component {
    static template = "l10n_cr_invoice.DocumentStatePopover";
    static props = {
        close: Function,
        onClose: Function,
        copyText: Function,
        message: String,
    };
}

export class L10nCrDocumentState extends SelectionField {
    static template = "l10n_cr_invoice.DocumentState";

    setup() {
        super.setup();
        this.popover = useService("popover");
        this.notification = useService("notification");
    }

    get message() {
        return this.props.record.data.l10n_cr_message_detail;
    }

    copyText() {
        navigator.clipboard.writeText(this.message);
        this.notification.add(_t("Text copied"), { type: "success" });
        this.popoverCloseFn();
        this.popoverCloseFn = null;
    }

    showMessagePopover(ev) {
        const close = () => {
            this.popoverCloseFn();
            this.popoverCloseFn = null;
        };

        if (this.popoverCloseFn) {
            close();
            return;
        }

        this.popoverCloseFn = this.popover.add(
            ev.currentTarget,
            DocumentStatePopover,
            {
                message: this.message,
                copyText: this.copyText.bind(this),
                onClose: close,
            },
            {
                closeOnClickAway: true,
                position: "top",
            },
        );
    }
}

registry.category("fields").add("l10n_cr_document_state", {
    ...selectionField,
    component: L10nCrDocumentState,
});
