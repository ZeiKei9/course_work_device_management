import csv

from django.http import HttpResponse


def export_devices_to_csv(queryset):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="devices.csv"'
    response.write("\ufeff".encode("utf8"))

    writer = csv.writer(response)
    writer.writerow(
        [
            "ID",
            "Name",
            "Serial Number",
            "Inventory Number",
            "Category",
            "Brand",
            "Status",
            "Condition",
            "Location",
            "Purchase Date",
            "Purchase Price",
            "Warranty Until",
            "Created At",
        ]
    )

    for device in queryset:
        writer.writerow(
            [
                device.id,
                device.name,
                device.serial_number,
                device.inventory_number,
                device.category.name if device.category else "",
                device.brand.name if device.brand else "",
                device.get_status_display(),
                device.get_condition_display(),
                device.location.name if device.location else "",
                device.purchase_date,
                device.purchase_price,
                device.warranty_until,
                device.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            ]
        )

    return response


def export_loans_to_csv(queryset):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="loans.csv"'
    response.write("\ufeff".encode("utf8"))

    writer = csv.writer(response)
    writer.writerow(
        [
            "ID",
            "User",
            "Device",
            "Serial Number",
            "Manager",
            "Loaned At",
            "Due Date",
            "Status",
        ]
    )

    for loan in queryset:
        writer.writerow(
            [
                loan.id,
                loan.user.username,
                loan.device.name,
                loan.device.serial_number,
                loan.manager.username if loan.manager else "",
                loan.loaned_at.strftime("%Y-%m-%d %H:%M:%S"),
                loan.due_date.strftime("%Y-%m-%d %H:%M:%S"),
                loan.get_status_display(),
            ]
        )

    return response
