# Private Claims

A private claim may show that a valid domain is assigned while keeping the holder identity out of the public registry.

Public records for private claims must use:

- `status: "assigned"`
- `assignment_type: "private_owner"`
- `holder.visibility: "private"`
- `holder.public_label: null`
- A pseudonymous `holder_ref`, such as `holder_7FQ3M2`

Maintainers may know the claimant through a private process. Do not commit that private mapping to this repository.

Do not include raw emails, phone numbers, postal addresses, or other private identity details in registry JSON.
